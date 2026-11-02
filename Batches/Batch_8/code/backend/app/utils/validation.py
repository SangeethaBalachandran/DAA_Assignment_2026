from typing import List, Tuple, Dict
from fastapi import HTTPException
from ..schemas.compression import SymbolFrequency

def validate_and_normalize_frequencies(
    frequencies: List[SymbolFrequency]
) -> List[Tuple[str, float, float]]:
    """
    Validates input frequencies, rejects invalid inputs, and normalizes into probabilities.
    Returns list of tuples: (symbol, frequency, probability).
    """
    if not frequencies or len(frequencies) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 distinct symbols are required to build a codebook."
        )

    # Check for duplicate symbols
    symbols = [item.symbol.strip() for item in frequencies]
    if len(symbols) != len(set(symbols)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate symbols found in input distribution."
        )

    for item in frequencies:
        if not item.symbol.strip():
            raise HTTPException(status_code=400, detail="Symbol identifier cannot be empty.")
        if item.frequency < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Frequency for symbol '{item.symbol}' cannot be negative: {item.frequency}"
            )

    total_freq = sum(item.frequency for item in frequencies)
    if total_freq <= 0:
        raise HTTPException(
            status_code=400,
            detail="Sum of frequencies must be strictly greater than 0."
        )

    result = []
    prob_sum = 0.0
    for item in frequencies:
        p = item.frequency / total_freq
        prob_sum += p
        result.append((item.symbol.strip(), float(item.frequency), p))

    # Verify normalization within float precision
    if abs(prob_sum - 1.0) > 1e-6:
        raise HTTPException(
            status_code=400,
            detail=f"Probability normalization failed: sum is {prob_sum}"
        )

    return result

def is_prefix_free(codebook_map: Dict[str, str]) -> Tuple[bool, str]:
    """
    Verifies that no codeword is a proper prefix of any other codeword.
    """
    items = list(codebook_map.items())
    for i in range(len(items)):
        sym1, code1 = items[i]
        for j in range(len(items)):
            if i == j:
                continue
            sym2, code2 = items[j]
            if code2.startswith(code1):
                return False, f"Codeword '{code1}' for '{sym1}' is a prefix of '{code2}' for '{sym2}'"
    return True, "Valid prefix-free code"

def check_kraft_inequality(lengths: List[int]) -> Tuple[bool, float]:
    """
    Calculates Kraft sum: sum(2^-l) <= 1.0.
    """
    kraft_sum = sum(2.0 ** (-l) for l in lengths if l > 0)
    is_valid = kraft_sum <= 1.000001
    return is_valid, kraft_sum

