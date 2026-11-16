from typing import List, Tuple, Dict, Optional
from ..schemas.compression import (
    SymbolFrequency, CompressionResponse, TwoQueueResponse, AlgorithmComparisonResponse
)
from ..utils.validation import validate_and_normalize_frequencies
from ..algorithms.huffman import build_huffman_tree
from ..algorithms.shannon_fano import build_shannon_fano
from ..algorithms.two_queue import build_two_queue_huffman
from ..algorithms.package_merge import run_package_merge, brute_force_optimal_cost

# Exact Ground Truth Assignment Distribution
DEFAULT_DISTRIBUTION = [
    SymbolFrequency(symbol="OK", frequency=52),
    SymbolFrequency(symbol="TEMP_HI", frequency=14),
    SymbolFrequency(symbol="TEMP_LO", frequency=11),
    SymbolFrequency(symbol="HUM", frequency=9),
    SymbolFrequency(symbol="VIB", frequency=7),
    SymbolFrequency(symbol="DOOR", frequency=4),
    SymbolFrequency(symbol="FAULT", frequency=2),
    SymbolFrequency(symbol="RESET", frequency=1),
]

# Mathematically Validated Counterexample Distributions
COUNTEREXAMPLE_5_SYMBOL = [
    SymbolFrequency(symbol="A", frequency=35),
    SymbolFrequency(symbol="B", frequency=17),
    SymbolFrequency(symbol="C", frequency=17),
    SymbolFrequency(symbol="D", frequency=16),
    SymbolFrequency(symbol="E", frequency=15),
]

COUNTEREXAMPLE_8_SYMBOL = [
    SymbolFrequency(symbol="OK", frequency=37),
    SymbolFrequency(symbol="TEMP_HI", frequency=16),
    SymbolFrequency(symbol="TEMP_LO", frequency=16),
    SymbolFrequency(symbol="HUM", frequency=9),
    SymbolFrequency(symbol="VIB", frequency=7),
    SymbolFrequency(symbol="DOOR", frequency=7),
    SymbolFrequency(symbol="FAULT", frequency=5),
    SymbolFrequency(symbol="RESET", frequency=3),
]

class CompressionService:
    def __init__(self):
        self._current_distribution: List[SymbolFrequency] = list(DEFAULT_DISTRIBUTION)

    def get_default_distribution(self) -> List[SymbolFrequency]:
        return list(DEFAULT_DISTRIBUTION)

    def get_counterexample_distribution(self, variant: str = "8-symbol") -> List[SymbolFrequency]:
        if variant == "5-symbol":
            return list(COUNTEREXAMPLE_5_SYMBOL)
        return list(COUNTEREXAMPLE_8_SYMBOL)

    def generate_huffman(
        self,
        frequencies: Optional[List[SymbolFrequency]] = None,
        fixed_bits: int = 3
    ) -> CompressionResponse:
        items = frequencies or self._current_distribution
        normalized = validate_and_normalize_frequencies(items)
        return build_huffman_tree(normalized, fixed_bits=fixed_bits)

    def generate_shannon_fano(
        self,
        frequencies: Optional[List[SymbolFrequency]] = None,
        fixed_bits: int = 3
    ) -> CompressionResponse:
        items = frequencies or self._current_distribution
        normalized = validate_and_normalize_frequencies(items)
        return build_shannon_fano(normalized, fixed_bits=fixed_bits)

    def generate_two_queue(
        self,
        frequencies: Optional[List[SymbolFrequency]] = None,
        fixed_bits: int = 3
    ) -> TwoQueueResponse:
        items = frequencies or self._current_distribution
        normalized = validate_and_normalize_frequencies(items)
        return build_two_queue_huffman(normalized, fixed_bits=fixed_bits)

    def generate_package_merge(
        self,
        frequencies: Optional[List[SymbolFrequency]] = None,
        max_length: int = 4,
        fixed_bits: int = 3
    ) -> CompressionResponse:
        items = frequencies or self._current_distribution
        normalized = validate_and_normalize_frequencies(items)
        return run_package_merge(normalized, max_length=max_length, fixed_bits=fixed_bits)

    def compare_algorithms(
        self,
        frequencies: Optional[List[SymbolFrequency]] = None,
        fixed_bits: int = 3
    ) -> AlgorithmComparisonResponse:
        items = frequencies or self._current_distribution
        normalized = validate_and_normalize_frequencies(items)

        resp_huff = build_huffman_tree(normalized, fixed_bits=fixed_bits)
        resp_sf = build_shannon_fano(normalized, fixed_bits=fixed_bits)
        resp_tq = build_two_queue_huffman(normalized, fixed_bits=fixed_bits)

        diff = round(resp_sf.average_length - resp_huff.average_length, 4)
        is_counter = diff > 0.0001

        if is_counter:
            explanation = (
                f"Shannon-Fano is strictly SUBOPTIMAL by +{diff:.4f} bits/message "
                f"({resp_sf.average_length:.4f} vs {resp_huff.average_length:.4f} bits). "
                f"This occurs because Shannon-Fano makes a top-down greedy partition that balances "
                f"subgroup weights at the root level, prematurely pushing high-frequency symbols into deeper branches. "
                f"Huffman's bottom-up greedy merge guarantees global optimality."
            )
        else:
            explanation = (
                f"On this distribution, Shannon-Fano and Huffman achieve identical average code length "
                f"({resp_huff.average_length:.4f} bits) because the top-down frequency split coincidentally "
                f"aligns with the bottom-up tree root. Load the validated Counterexample to observe "
                f"strict suboptimality."
            )

        return AlgorithmComparisonResponse(
            huffman=resp_huff,
            shannon_fano=resp_sf,
            two_queue=resp_tq,
            is_counterexample=is_counter,
            length_difference=diff,
            explanation=explanation
        )

compression_service = CompressionService()

