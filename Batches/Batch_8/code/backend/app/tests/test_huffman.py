import pytest
from ..schemas.compression import SymbolFrequency
from ..services.compression_service import compression_service, DEFAULT_DISTRIBUTION
from ..utils.validation import is_prefix_free, check_kraft_inequality

def test_huffman_default_distribution():
    resp = compression_service.generate_huffman()
    assert resp.average_length == 2.2000
    assert resp.max_codeword_length == 6
    assert resp.hardware_compatible is False  # Violates 4-bit register!
    assert resp.compression_ratio == pytest.approx(1.3636, rel=1e-3)
    assert resp.bandwidth_savings_pct == pytest.approx(26.67, rel=1e-2)
    assert resp.kraft_sum == pytest.approx(1.0, abs=1e-5)

    # Validate prefix-free property
    valid, msg = is_prefix_free(resp.codebook_map)
    assert valid is True, msg

def test_huffman_tree_structure():
    resp = compression_service.generate_huffman()
    assert resp.tree is not None
    assert resp.tree.weight == 100.0
    # Root should have 2 children
    assert resp.tree.children is not None
    assert len(resp.tree.children) == 2

def test_huffman_rejects_invalid_inputs():
    with pytest.raises(Exception):
        compression_service.generate_huffman([
            SymbolFrequency(symbol="ONLY_ONE", frequency=100)
        ])

    with pytest.raises(Exception):
        compression_service.generate_huffman([
            SymbolFrequency(symbol="A", frequency=-10),
            SymbolFrequency(symbol="B", frequency=20)
        ])

