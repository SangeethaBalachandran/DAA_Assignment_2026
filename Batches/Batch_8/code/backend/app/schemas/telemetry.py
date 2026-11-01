from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TelemetryConfig(BaseModel):
    message_rate: float = Field(default=40.0, ge=1.0, le=1000.0, description="Aggregate messages/second")
    sensor_population: int = Field(default=5000, ge=1, description="Total sensor population")
    channel_capacity: float = Field(default=9600.0, ge=100.0, description="Link capacity in bits/second")
    fixed_bits: int = Field(default=3, ge=1, le=8, description="Legacy fixed-length bits/symbol")
    random_seed: Optional[int] = Field(default=None, description="Reproducible random seed")
    traffic_profile: Optional[str] = Field(default="dynamic", description="Simulation traffic profile: dynamic, normal, high_temp, high_vib, fault_heavy")

class NetworkMetrics(BaseModel):
    message_rate: float
    channel_capacity: float
    original_bitrate: float
    compressed_bitrate: float
    bandwidth_saved_bps: float
    bandwidth_saved_bph: float
    original_utilization_pct: float
    compressed_utilization_pct: float
    percentage_savings: float
    available_capacity_bps: float
    congestion_status: str
    overhead_framing_bps: float
    overhead_broadcast_bps: float

class LiveTelemetryPacket(BaseModel):
    timestamp: float
    sequence_id: int
    sensor_id: int
    symbol: str
    original_bits: int
    codeword: str
    compressed_bits: int
    channel_load_bps: float
    utilization_pct: float
    value: Optional[float] = Field(default=None, description="Simulated sensor reading value")

class SimulationStatus(BaseModel):
    is_running: bool
    is_paused: bool
    messages_transmitted: int
    cumulative_original_bits: int
    cumulative_compressed_bits: int
    cumulative_bits_saved: int
    current_bitrate_bps: float
    elapsed_seconds: float
    simulated_duration: str

class CodebookBroadcastRequest(BaseModel):
    target_version: Optional[str] = None
    algorithm: Optional[str] = "package_merge"
    receiver_count: int = Field(default=5000, ge=1)
    simulated_loss_rate: float = Field(default=0.015, ge=0.0, le=0.5)

class ReceiverStatus(BaseModel):
    receiver_id: int
    synchronized: bool
    current_version: str
    latency_ms: float
    retries: int

class CodebookBroadcastResponse(BaseModel):
    version: str
    algorithm: str
    broadcast_timestamp: float
    payload_bits: int
    framing_bits: int
    total_broadcast_bits: int
    amortized_bps: float
    receivers_total: int
    receivers_acked: int
    receivers_failed: int
    sync_percentage: float
    sample_receivers: List[ReceiverStatus]

