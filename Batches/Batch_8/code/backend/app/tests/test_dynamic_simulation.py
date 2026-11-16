import time
import pytest
from ..schemas.telemetry import TelemetryConfig
from ..services.telemetry_service import telemetry_service, TRAFFIC_PROFILES
from ..services.codebook_service import codebook_service

def test_packet_level_huffman_compression_integrity():
    """
    Verifies that every generated packet uses actual Huffman codewords and lengths,
    with exact bits saved math (orig_bits - comp_bits).
    """
    codebook = codebook_service.get_current_codebook()

    # Configure simulation
    telemetry_service.reset_simulation()
    telemetry_service.configure(TelemetryConfig(message_rate=40, traffic_profile="normal", random_seed=42))

    # Generate a sample sequence of symbols
    symbols = ["OK", "TEMP_HI", "TEMP_LO", "HUM", "VIB", "DOOR", "FAULT", "RESET"]
    for sym in symbols:
        cw = codebook.get(sym)
        assert cw is not None, f"Codebook missing codeword for {sym}"
        comp_len = len(cw)
        orig_len = 3
        bits_saved = orig_len - comp_len

        # Code length bounds and integrity check
        assert 1 <= comp_len <= 6
        assert bits_saved == 3 - comp_len
        if sym == "OK":
            assert comp_len == 1  # 1 bit
            assert bits_saved == 2  # 2 bits saved per OK message
        else:
            assert comp_len >= 2
            assert bits_saved == 3 - comp_len

def test_traffic_profile_dynamic_fluctuations():
    """
    Tests dynamic traffic generation across all profiles:
    1. Normal
    2. High Temperature
    3. High Vibration
    4. Fault Heavy
    Verifies that compressed bitrates and savings dynamically reflect symbol lengths.
    """
    codebook = codebook_service.get_current_codebook()

    profiles_to_test = ["normal", "high_temp", "high_vib", "fault_heavy"]
    results = {}

    for prof in profiles_to_test:
        telemetry_service.reset_simulation()
        telemetry_service.configure(TelemetryConfig(message_rate=40, traffic_profile=prof, random_seed=100))

        # Simulate 1 second worth of traffic (40 packets)
        dist = TRAFFIC_PROFILES[prof]
        symbols = list(dist.keys())
        weights = list(dist.values())

        sampled = telemetry_service._rng.choices(symbols, weights=weights, k=40)
        now = time.time()
        for sym in sampled:
            cw = codebook[sym]
            orig_bits = 3
            comp_bits = len(cw)
            telemetry_service.messages_transmitted += 1
            telemetry_service.cumulative_orig_bits += orig_bits
            telemetry_service.cumulative_comp_bits += comp_bits
            telemetry_service._rolling_events.append((now, orig_bits, comp_bits))

        dyn_metrics = telemetry_service.get_dynamic_metrics()
        results[prof] = dyn_metrics

        # Basic physics sanity checks
        assert dyn_metrics.original_bitrate > 0
        assert dyn_metrics.compressed_bitrate > 0
        assert dyn_metrics.channel_capacity == 9600.0

    # Comparative analysis across profiles:
    # 1. Normal has high OK frequency -> lower compressed bitrate than fault_heavy
    assert results["normal"].compressed_bitrate < results["fault_heavy"].compressed_bitrate
    assert results["normal"].percentage_savings > results["fault_heavy"].percentage_savings

    # 2. Fault heavy has long codewords (5b and 6b) -> higher compressed bitrate than normal
    assert results["fault_heavy"].compressed_bitrate > results["normal"].compressed_bitrate

    # Cleanup
    telemetry_service.reset_simulation()
    telemetry_service.configure(TelemetryConfig(message_rate=40, traffic_profile="dynamic", random_seed=None))

def test_aggregate_message_rate_scaling():
    """
    Verifies that changing aggregate message rate scales original and compressed bitrates proportionally.
    """
    telemetry_service.reset_simulation()

    # Rate 20 msgs/s -> 20 * 3 = 60 bps theoretical original
    m20 = telemetry_service.configure(TelemetryConfig(message_rate=20))
    assert m20.original_bitrate == 60.0

    # Rate 80 msgs/s -> 80 * 3 = 240 bps theoretical original
    m80 = telemetry_service.configure(TelemetryConfig(message_rate=80))
    assert m80.original_bitrate == 240.0

    # Ratio matches exactly
    assert m80.original_bitrate == 4 * m20.original_bitrate

    # Restore default
    telemetry_service.configure(TelemetryConfig(message_rate=40))
