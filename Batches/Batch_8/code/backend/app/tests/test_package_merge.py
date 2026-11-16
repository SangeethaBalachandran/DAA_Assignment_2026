import pytest
from ..schemas.compression import SymbolFrequency
from ..services.compression_service import compression_service, DEFAULT_DISTRIBUTION
from ..algorithms.package_merge import brute_force_optimal_cost
from ..utils.validation import validate_and_normalize_frequencies, is_prefix_free

def test_package_merge_respects_max_length_4():
    resp = compression_service.generate_package_merge(max_length=4)
    assert resp.average_length == 2.3000
    assert resp.max_codeword_length <= 4
    assert resp.hardware_compatible is True
    assert resp.kraft_sum <= 1.00001

    valid, msg = is_prefix_free(resp.codebook_map)
    assert valid is True, msg

def test_package_merge_matches_brute_force_optimal():
    """
    Validates Package-Merge output against independent exhaustive search validator.
    """
    normalized = validate_and_normalize_frequencies(DEFAULT_DISTRIBUTION)
    bf_cost = brute_force_optimal_cost(normalized, max_length=4)
    pm_resp = compression_service.generate_package_merge(max_length=4)

    assert bf_cost == pytest.approx(2.3000, abs=1e-4)
    assert pm_resp.average_length == pytest.approx(bf_cost, abs=1e-4)

def test_package_merge_infeasible_constraint():
    # 8 symbols cannot fit in max_length 2 (2^2 = 4 max symbols)
    with pytest.raises(Exception):
        compression_service.generate_package_merge(max_length=2)

