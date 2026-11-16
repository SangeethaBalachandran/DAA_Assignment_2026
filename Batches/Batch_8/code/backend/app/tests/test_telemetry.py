import pytest
from ..schemas.telemetry import TelemetryConfig, CodebookBroadcastRequest
from ..services.telemetry_service import telemetry_service
from ..services.codebook_service import codebook_service

def test_telemetry_network_math():
    metrics = telemetry_service.get_theoretical_metrics()
    assert metrics.message_rate == 40.0
    assert metrics.original_bitrate == 120.0
    assert metrics.compressed_bitrate == pytest.approx(92.0, abs=0.1)  # 40 * 2.3 = 92.0
    assert metrics.bandwidth_saved_bps == pytest.approx(28.0, abs=0.1)
    assert metrics.bandwidth_saved_bph == pytest.approx(100800.0, abs=10.0)
    assert metrics.percentage_savings == pytest.approx(23.33, abs=0.1)

def test_one_hour_simulation_projection():
    projection = telemetry_service.simulate_one_hour()
    assert projection["total_messages"] == 144000
    assert projection["original_bits"] == 432000
    assert projection["huffman_bits"] == 316800
    assert projection["huffman_bits_saved"] == 115200
    assert projection["package_merge_bits"] == 331200
    assert projection["package_merge_bits_saved"] == 100800

def test_codebook_broadcast_simulation():
    req = CodebookBroadcastRequest(receiver_count=5000, simulated_loss_rate=0.01)
    resp = codebook_service.broadcast_codebook(req)
    assert resp.receivers_total == 5000
    assert resp.receivers_acked > 4800
    assert resp.sync_percentage > 96.0
    assert resp.payload_bits == 80
    assert resp.total_broadcast_bits == 112

