import pytest
from ..schemas.compression import SymbolFrequency
from ..services.compression_service import (
    compression_service, COUNTEREXAMPLE_5_SYMBOL, COUNTEREXAMPLE_8_SYMBOL
)
from ..utils.validation import is_prefix_free

def test_shannon_fano_default_distribution():
    resp = compression_service.generate_shannon_fano()
    assert resp.average_length == 2.2000
    valid, msg = is_prefix_free(resp.codebook_map)
    assert valid is True, msg

def test_shannon_fano_5_symbol_counterexample():
    """
    Validates classic counterexample [A:35, B:17, C:17, D:16, E:15].
    Shannon-Fano must yield strictly higher average code length than Huffman.
    """
    comp = compression_service.compare_algorithms(COUNTEREXAMPLE_5_SYMBOL)
    assert comp.is_counterexample is True
    assert comp.huffman.average_length == 2.3000
    assert comp.shannon_fano.average_length == 2.3100
    assert comp.length_difference == pytest.approx(0.0100, abs=1e-4)
    assert comp.shannon_fano.average_length > comp.huffman.average_length

def test_shannon_fano_8_symbol_counterexample():
    """
    Validates 8-symbol IoT counterexample [37, 16, 16, 9, 7, 7, 5, 3].
    """
    comp = compression_service.compare_algorithms(COUNTEREXAMPLE_8_SYMBOL)
    assert comp.is_counterexample is True
    assert comp.huffman.average_length == 2.6500
    assert comp.shannon_fano.average_length == 2.6900
    assert comp.length_difference == pytest.approx(0.0400, abs=1e-4)
    assert comp.shannon_fano.average_length > comp.huffman.average_length

