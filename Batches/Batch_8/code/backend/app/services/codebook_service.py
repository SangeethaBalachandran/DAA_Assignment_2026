import time
import random
from typing import Dict, List, Optional, Tuple
from ..schemas.telemetry import (
    CodebookBroadcastRequest, CodebookBroadcastResponse, ReceiverStatus
)
from .compression_service import compression_service

class CodebookService:
    def __init__(self):
        self.current_version = "v1.0.0"
        self.codebook_versions: Dict[str, Dict[str, str]] = {}
        self.version_history: List[Dict] = []
        self.receiver_table: Dict[int, str] = {i: "v1.0.0" for i in range(1, 5001)}

        # Initialize with default package-merge codebook
        pm_resp = compression_service.generate_package_merge()
        self.codebook_versions[self.current_version] = pm_resp.codebook_map

    def get_current_codebook(self) -> Dict[str, str]:
        return self.codebook_versions.get(self.current_version, {})

    def broadcast_codebook(self, req: CodebookBroadcastRequest) -> CodebookBroadcastResponse:
        """
        Simulates broadcasting an updated codebook to all receivers.
        Models transmission latency, random packet loss requiring retry, and ACK receipts.
        """
        # Create new version tag if not provided
        parts = self.current_version.replace("v", "").split(".")
        new_patch = int(parts[2]) + 1
        new_version = req.target_version or f"v{parts[0]}.{parts[1]}.{new_patch}"

        # Generate codebook using requested algorithm
        if req.algorithm == "huffman":
            resp = compression_service.generate_huffman()
        else:
            resp = compression_service.generate_package_merge()

        self.current_version = new_version
        self.codebook_versions[new_version] = resp.codebook_map

        # Simulate ACK across receivers
        total_rx = req.receiver_count
        loss_rate = req.simulated_loss_rate
        acked = 0
        failed = 0
        sample_receivers: List[ReceiverStatus] = []

        # Deterministic simulation with seed for repeatability
        rng = random.Random(42 + int(time.time()) % 1000)

        for rx_id in range(1, total_rx + 1):
            is_lost = rng.random() < loss_rate
            if not is_lost:
                acked += 1
                self.receiver_table[rx_id] = new_version
                status = ReceiverStatus(
                    receiver_id=rx_id,
                    synchronized=True,
                    current_version=new_version,
                    latency_ms=round(rng.uniform(12.0, 48.0), 2),
                    retries=0
                )
            else:
                # 1 retry attempt
                if rng.random() > 0.3:
                    acked += 1
                    self.receiver_table[rx_id] = new_version
                    status = ReceiverStatus(
                        receiver_id=rx_id,
                        synchronized=True,
                        current_version=new_version,
                        latency_ms=round(rng.uniform(60.0, 120.0), 2),
                        retries=1
                    )
                else:
                    failed += 1
                    status = ReceiverStatus(
                        receiver_id=rx_id,
                        synchronized=False,
                        current_version="v1.0.0",
                        latency_ms=round(rng.uniform(150.0, 250.0), 2),
                        retries=2
                    )

            if rx_id <= 20:  # Sample 20 receivers for frontend display
                sample_receivers.append(status)

        # Broadcast packet sizing: 8 symbols * 10 bits = 80 bits payload
        payload_bits = len(resp.codebook) * 10
        framing_bits = 32  # SOF + Length + CRC16
        total_bits = payload_bits + framing_bits
        amortized_bps = round(total_bits / 3600.0, 5)

        sync_pct = round((acked / total_rx) * 100.0, 2)

        record = {
            "version": new_version,
            "algorithm": req.algorithm,
            "timestamp": time.time(),
            "sync_percentage": sync_pct,
            "acked": acked,
            "failed": failed
        }
        self.version_history.append(record)

        return CodebookBroadcastResponse(
            version=new_version,
            algorithm=req.algorithm or "package_merge",
            broadcast_timestamp=time.time(),
            payload_bits=payload_bits,
            framing_bits=framing_bits,
            total_broadcast_bits=total_bits,
            amortized_bps=amortized_bps,
            receivers_total=total_rx,
            receivers_acked=acked,
            receivers_failed=failed,
            sync_percentage=sync_pct,
            sample_receivers=sample_receivers
        )

    def verify_version(self, version: Optional[str]) -> Tuple[bool, str]:
        if not version:
            return True, "No version specified; assuming active"
        if version != self.current_version:
            return False, f"Codebook version mismatch: active gateway version is '{self.current_version}', but receiver used outdated version '{version}'. Re-synchronization required."
        return True, "Codebook version verified"

codebook_service = CodebookService()

