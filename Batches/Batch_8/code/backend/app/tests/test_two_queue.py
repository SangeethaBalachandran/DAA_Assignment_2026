import pytest
from ..schemas.compression import SymbolFrequency
from ..services.compression_service import compression_service, DEFAULT_DISTRIBUTION

def test_two_queue_equivalence_with_min_heap():
    """
    Validates that Two-Queue and Min-Heap Huffman yield identical optimal weighted path lengths.
    """
    huff_resp = compression_service.generate_huffman()
    tq_resp = compression_service.generate_two_queue()

    assert tq_resp.average_length == pytest.approx(huff_resp.average_length, abs=1e-6)
    assert tq_resp.average_length == 2.2000
    assert len(tq_resp.steps) == len(DEFAULT_DISTRIBUTION) - 1

def test_two_queue_step_recording():
    tq_resp = compression_service.generate_two_queue()
    assert len(tq_resp.steps) == 7
    # First step should merge smallest frequencies: RESET(1) and FAULT(2) -> 3
    s1 = tq_resp.steps[0]
    assert s1.merged_weight == 3.0
    assert "RESET" in s1.popped[0] or "RESET" in s1.popped[1]
    assert "FAULT" in s1.popped[0] or "FAULT" in s1.popped[1]

