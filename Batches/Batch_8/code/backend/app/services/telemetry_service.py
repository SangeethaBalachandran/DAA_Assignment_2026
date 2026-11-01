import time
import random
import asyncio
from collections import deque
from typing import List, Dict, Optional, Set, Tuple
from fastapi import WebSocket
from ..schemas.telemetry import (
    TelemetryConfig, SimulationStatus, LiveTelemetryPacket, NetworkMetrics
)
from ..utils.metrics import calculate_network_metrics
from .compression_service import compression_service
from .codebook_service import codebook_service

TRAFFIC_PROFILES = {
    "normal": {
        "OK": 52, "TEMP_HI": 14, "TEMP_LO": 11, "HUM": 9, "VIB": 7, "DOOR": 4, "FAULT": 2, "RESET": 1
    },
    "high_temp": {
        "TEMP_HI": 50, "TEMP_LO": 20, "OK": 16, "HUM": 5, "VIB": 4, "DOOR": 3, "FAULT": 1, "RESET": 1
    },
    "high_vib": {
        "VIB": 52, "HUM": 22, "OK": 14, "TEMP_HI": 4, "TEMP_LO": 4, "DOOR": 2, "FAULT": 1, "RESET": 1
    },
    "fault_heavy": {
        "FAULT": 35, "RESET": 25, "DOOR": 20, "VIB": 8, "HUM": 6, "TEMP_HI": 3, "TEMP_LO": 2, "OK": 1
    }
}

class TelemetryService:
    def __init__(self):
        self.config = TelemetryConfig()
        self.is_running = False
        self.is_paused = False
        self.messages_transmitted = 0
        self.cumulative_orig_bits = 0
        self.cumulative_comp_bits = 0
        self.sequence_counter = 1
        self.start_timestamp = 0.0
        self.active_websockets: Set[WebSocket] = set()
        self._simulation_task: Optional[asyncio.Task] = None
        self._rng = random.Random(42)

        # Dynamic rolling window state (1.0 second duration)
        self.window_duration = 1.0
        self._rolling_events: deque[Tuple[float, int, int]] = deque()
        self._dynamic_phase = "normal"
        self._phase_switch_time = 0.0

    def configure(self, new_config: TelemetryConfig) -> NetworkMetrics:
        self.config = new_config
        if new_config.random_seed is not None:
            self._rng = random.Random(new_config.random_seed)
        return self.get_theoretical_metrics()

    def get_theoretical_metrics(self) -> NetworkMetrics:
        resp = compression_service.generate_package_merge()
        return calculate_network_metrics(
            message_rate=self.config.message_rate,
            channel_capacity=self.config.channel_capacity,
            fixed_bits=self.config.fixed_bits,
            avg_compressed_bits=resp.average_length
        )

    def get_dynamic_metrics(self) -> NetworkMetrics:
        now = time.time()
        cutoff = now - self.window_duration
        while self._rolling_events and self._rolling_events[0][0] < cutoff:
            self._rolling_events.popleft()

        if not self._rolling_events:
            return self.get_theoretical_metrics()

        total_orig = sum(e[1] for e in self._rolling_events)
        total_comp = sum(e[2] for e in self._rolling_events)
        oldest_ts = self._rolling_events[0][0]
        dt = max(0.2, now - oldest_ts)

        orig_bitrate = round(total_orig / dt, 1)
        comp_bitrate = round(total_comp / dt, 1)
        saved_bps = round(orig_bitrate - comp_bitrate, 1)
        saved_bph = round(saved_bps * 3600, 1)

        orig_util = round((orig_bitrate / self.config.channel_capacity) * 100.0, 3)
        comp_util = round((comp_bitrate / self.config.channel_capacity) * 100.0, 3)

        savings_pct = round(((total_orig - total_comp) / total_orig) * 100.0, 2) if total_orig > 0 else 0.0
        avail = round(max(0.0, self.config.channel_capacity - comp_bitrate), 1)

        congestion = 'OPTIMAL' if comp_util < 70 else ('CONGESTED' if comp_util < 90 else 'CRITICAL')

        return NetworkMetrics(
            message_rate=round(len(self._rolling_events) / dt, 1),
            channel_capacity=self.config.channel_capacity,
            original_bitrate=orig_bitrate,
            compressed_bitrate=comp_bitrate,
            bandwidth_saved_bps=saved_bps,
            bandwidth_saved_bph=saved_bph,
            original_utilization_pct=orig_util,
            compressed_utilization_pct=comp_util,
            percentage_savings=savings_pct,
            available_capacity_bps=avail,
            congestion_status=congestion,
            overhead_framing_bps=round((len(self._rolling_events) / dt) * 0.75, 2),
            overhead_broadcast_bps=0.0311
        )

    def get_status(self) -> SimulationStatus:
        elapsed = (time.time() - self.start_timestamp) if (self.is_running and self.start_timestamp > 0) else 0.0
        saved = max(0, self.cumulative_orig_bits - self.cumulative_comp_bits)
        current_bps = (self.cumulative_comp_bits / elapsed) if elapsed > 0 else 0.0

        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        dur_str = f"{mins:02d}:{secs:02d}"

        return SimulationStatus(
            is_running=self.is_running,
            is_paused=self.is_paused,
            messages_transmitted=self.messages_transmitted,
            cumulative_original_bits=self.cumulative_orig_bits,
            cumulative_compressed_bits=self.cumulative_comp_bits,
            cumulative_bits_saved=saved,
            current_bitrate_bps=round(current_bps, 2),
            elapsed_seconds=round(elapsed, 2),
            simulated_duration=dur_str
        )

    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_timestamp = time.time()
            self._phase_switch_time = time.time() + 8.0
            try:
                loop = asyncio.get_running_loop()
                if not self._simulation_task or self._simulation_task.done():
                    self._simulation_task = loop.create_task(self._simulation_loop())
            except RuntimeError:
                pass

    def pause_simulation(self):
        self.is_paused = True

    def resume_simulation(self):
        self.is_paused = False

    def reset_simulation(self):
        self.is_running = False
        self.is_paused = False
        self.messages_transmitted = 0
        self.cumulative_orig_bits = 0
        self.cumulative_comp_bits = 0
        self.sequence_counter = 1
        self.start_timestamp = 0.0
        self._rolling_events.clear()
        if self._simulation_task and not self._simulation_task.done():
            self._simulation_task.cancel()

    def simulate_one_hour(self) -> Dict[str, Any]:
        hour_messages = int(self.config.message_rate * 3600)
        resp_pm = compression_service.generate_package_merge()
        resp_huff = compression_service.generate_huffman()

        orig_bits = hour_messages * self.config.fixed_bits
        huff_bits = round(hour_messages * resp_huff.average_length)
        pm_bits = round(hour_messages * resp_pm.average_length)

        huff_saved = orig_bits - huff_bits
        pm_saved = orig_bits - pm_bits

        return {
            "duration_hours": 1,
            "total_messages": hour_messages,
            "original_bits": orig_bits,
            "original_bytes": round(orig_bits / 8.0, 1),
            "huffman_bits": huff_bits,
            "huffman_bytes": round(huff_bits / 8.0, 1),
            "huffman_bits_saved": huff_saved,
            "huffman_savings_pct": round((huff_saved / orig_bits) * 100.0, 2),
            "package_merge_bits": pm_bits,
            "package_merge_bytes": round(pm_bits / 8.0, 1),
            "package_merge_bits_saved": pm_saved,
            "package_merge_savings_pct": round((pm_saved / orig_bits) * 100.0, 2),
            "hardware_compatible_savings_pct": 23.33,
            "channel_capacity_bph": int(self.config.channel_capacity * 3600)
        }

    async def register_websocket(self, ws: WebSocket):
        await ws.accept()
        self.active_websockets.add(ws)

    def unregister_websocket(self, ws: WebSocket):
        self.active_websockets.discard(ws)

    async def broadcast_ws(self, payload: dict):
        dead_sockets = set()
        for ws in self.active_websockets:
            try:
                await ws.send_json(payload)
            except Exception:
                dead_sockets.add(ws)
        for ds in dead_sockets:
            self.active_websockets.discard(ds)

    def _generate_sensor_value(self, symbol: str) -> float:
        if symbol == "OK":
            return round(self._rng.uniform(20.0, 25.0), 1)
        elif symbol == "TEMP_HI":
            return round(self._rng.uniform(75.0, 98.5), 1)
        elif symbol == "TEMP_LO":
            return round(self._rng.uniform(-15.0, 5.0), 1)
        elif symbol == "HUM":
            return round(self._rng.uniform(75.0, 95.0), 1)
        elif symbol == "VIB":
            return round(self._rng.uniform(0.045, 0.180), 3)
        elif symbol == "DOOR":
            return 1.0
        elif symbol == "FAULT":
            return float(self._rng.choice([501, 502, 503, 504]))
        elif symbol == "RESET":
            return 1.0
        return 0.0

    async def _simulation_loop(self):
        """
        Background loop emitting telemetry packets according to dynamic probability distributions.
        Calculates instantaneous bitrates and compression savings from real rolling windows.
        """
        batch_interval = 0.25  # 250 ms update cadence

        while self.is_running:
            if self.is_paused:
                await asyncio.sleep(0.1)
                continue

            now = time.time()
            # Handle dynamic traffic profile transitions
            prof_name = self.config.traffic_profile or "dynamic"
            if prof_name == "dynamic":
                if now > self._phase_switch_time:
                    # Switch phase: 60% normal, 15% high temp, 15% high vib, 10% fault heavy
                    self._dynamic_phase = self._rng.choices(
                        ["normal", "high_temp", "high_vib", "fault_heavy"],
                        weights=[60, 15, 15, 10]
                    )[0]
                    duration = self._rng.uniform(6.0, 14.0)
                    self._phase_switch_time = now + duration
                active_dist = TRAFFIC_PROFILES[self._dynamic_phase]
            else:
                active_dist = TRAFFIC_PROFILES.get(prof_name, TRAFFIC_PROFILES["normal"])

            symbols = list(active_dist.keys())
            weights = list(active_dist.values())

            # Determine batch count based on aggregate message rate with Poisson jitter
            base_count = self.config.message_rate * batch_interval
            jitter = self._rng.choice([-1, 0, 1]) if base_count >= 4 else 0
            batch_count = max(1, int(round(base_count + jitter)))

            codebook = codebook_service.get_current_codebook()
            sampled_symbols = self._rng.choices(symbols, weights=weights, k=batch_count)
            packets: List[dict] = []

            for sym in sampled_symbols:
                cw = codebook.get(sym, "0")
                comp_bits = len(cw)
                orig_bits = self.config.fixed_bits
                sensor_id = self._rng.randint(1, self.config.sensor_population)
                reading_val = self._generate_sensor_value(sym)

                self.messages_transmitted += 1
                self.cumulative_orig_bits += orig_bits
                self.cumulative_comp_bits += comp_bits

                pkt_time = time.time()
                self._rolling_events.append((pkt_time, orig_bits, comp_bits))

                pkt = LiveTelemetryPacket(
                    timestamp=pkt_time,
                    sequence_id=self.sequence_counter,
                    sensor_id=sensor_id,
                    symbol=sym,
                    original_bits=orig_bits,
                    codeword=cw,
                    compressed_bits=comp_bits,
                    channel_load_bps=0.0,
                    utilization_pct=0.0,
                    value=reading_val
                )
                self.sequence_counter += 1
                packets.append(pkt.model_dump())

            # Prune events older than window
            dyn_metrics = self.get_dynamic_metrics()

            # Assign dynamic load metrics to packets
            for p in packets:
                p["channel_load_bps"] = dyn_metrics.compressed_bitrate
                p["utilization_pct"] = dyn_metrics.compressed_utilization_pct

            status = self.get_status().model_dump()

            ws_payload = {
                "type": "TELEMETRY_UPDATE",
                "packets": packets,
                "status": status,
                "metrics": dyn_metrics.model_dump()
            }
            await self.broadcast_ws(ws_payload)
            await asyncio.sleep(batch_interval)

telemetry_service = TelemetryService()
