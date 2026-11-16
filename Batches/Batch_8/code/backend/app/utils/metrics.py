import math
from typing import List, Dict, Tuple
from ..schemas.telemetry import NetworkMetrics

def calculate_entropy(probabilities: List[float]) -> float:
    """
    Shannon Information Entropy H(X) = -sum(p_i * log2(p_i))
    """
    ent = 0.0
    for p in probabilities:
        if p > 0:
            ent -= p * math.log2(p)
    return round(ent, 5)

def calculate_average_length(probabilities: List[float], lengths: List[int]) -> float:
    """
    Weighted average codeword length L = sum(p_i * l_i)
    """
    return round(sum(p * l for p, l in zip(probabilities, lengths)), 5)

def calculate_network_metrics(
    message_rate: float,
    channel_capacity: float,
    fixed_bits: int,
    avg_compressed_bits: float
) -> NetworkMetrics:
    """
    Calculates operational network bandwidth metrics:
    - Original bitrate
    - Compressed bitrate
    - Bandwidth saved
    - Bandwidth saved per hour
    - Link utilization
    - Channel headroom
    """
    orig_bitrate = message_rate * fixed_bits
    comp_bitrate = message_rate * avg_compressed_bits
    saved_bps = orig_bitrate - comp_bitrate
    saved_bph = saved_bps * 3600.0

    orig_util = (orig_bitrate / channel_capacity) * 100.0
    comp_util = (comp_bitrate / channel_capacity) * 100.0
    savings_pct = ((fixed_bits - avg_compressed_bits) / fixed_bits) * 100.0
    avail_cap = max(0.0, channel_capacity - comp_bitrate)

    # Congestion status threshold
    if comp_util > 85.0:
        congestion = "CRITICAL"
    elif comp_util > 50.0:
        congestion = "CONGESTED"
    else:
        congestion = "OPTIMAL"

    # Framing overhead model: 4 bytes per frame of 64 messages
    frames_per_sec = message_rate / 64.0
    overhead_framing = frames_per_sec * 32.0  # 32 bits framing per frame

    # Broadcast overhead model: 80 bits codebook broadcasted once per hour
    overhead_broadcast = 80.0 / 3600.0

    return NetworkMetrics(
        message_rate=round(message_rate, 2),
        channel_capacity=round(channel_capacity, 2),
        original_bitrate=round(orig_bitrate, 2),
        compressed_bitrate=round(comp_bitrate, 2),
        bandwidth_saved_bps=round(saved_bps, 2),
        bandwidth_saved_bph=round(saved_bph, 2),
        original_utilization_pct=round(orig_util, 3),
        compressed_utilization_pct=round(comp_util, 3),
        percentage_savings=round(savings_pct, 2),
        available_capacity_bps=round(avail_cap, 2),
        congestion_status=congestion,
        overhead_framing_bps=round(overhead_framing, 4),
        overhead_broadcast_bps=round(overhead_broadcast, 5)
    )

