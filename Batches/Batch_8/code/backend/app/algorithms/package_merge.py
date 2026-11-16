import time
from typing import List, Tuple, Dict, Optional, Any
from fastapi import HTTPException
from ..schemas.compression import (
    CodebookEntry, TreeNode, CompressionResponse
)
from ..utils.metrics import calculate_entropy, calculate_average_length
from ..utils.validation import check_kraft_inequality, is_prefix_free

def run_package_merge(
    normalized_items: List[Tuple[str, float, float]],
    max_length: int = 4,
    fixed_bits: int = 3
) -> CompressionResponse:
    """
    Implements the Package-Merge algorithm (Larmore & Hirschberg, 1990)
    for optimal length-limited prefix-free coding with constraint l_i <= max_length.
    """
    start_time = time.perf_counter()
    n = len(normalized_items)

    # 1. Feasibility check: Can n symbols fit in a tree of depth max_length?
    # Max leaves at depth L is 2^L.
    if n > (1 << max_length):
        raise HTTPException(
            status_code=400,
            detail=f"Infeasible constraint: {n} symbols cannot fit in a binary tree of maximum depth {max_length} (max capacity is 2^{max_length} = {1 << max_length} symbols)."
        )

    # 2. Sort symbols ascending by frequency
    sorted_items = sorted(normalized_items, key=lambda x: x[1])
    ops_count = len(sorted_items)

    # Represent items as: (weight, [indices_of_symbols_contained])
    base_items: List[Tuple[float, List[int]]] = [
        (freq, [i]) for i, (sym, freq, prob) in enumerate(sorted_items)
    ]

    P = list(base_items)

    # 3. Package and Merge iterations: levels 1 to max_length - 1
    for level in range(1, max_length):
        packages: List[Tuple[float, List[int]]] = []
        for i in range(0, len(P) - 1, 2):
            w = P[i][0] + P[i+1][0]
            indices = P[i][1] + P[i+1][1]
            packages.append((w, indices))
            ops_count += 1

        # Merge packages with base_items, maintaining sorted order
        merged: List[Tuple[float, List[int]]] = []
        i, j = 0, 0
        while i < len(packages) and j < len(base_items):
            ops_count += 1
            if packages[i][0] <= base_items[j][0]:
                merged.append(packages[i])
                i += 1
            else:
                merged.append(base_items[j])
                j += 1
        while i < len(packages):
            merged.append(packages[i])
            i += 1
        while j < len(base_items):
            merged.append(base_items[j])
            j += 1

        P = merged

    # 4. Select the first 2N - 2 items in P_{max_length}
    k = 2 * n - 2
    if len(P) < k:
        raise HTTPException(
            status_code=500,
            detail=f"Package-Merge error: Available packages ({len(P)}) less than required ({k})."
        )

    selected = P[:k]

    # 5. Extract codeword lengths
    lengths = [0] * n
    for item in selected:
        for idx in item[1]:
            lengths[idx] += 1

    # Verify all lengths satisfy length limit
    if any(l > max_length for l in lengths):
        raise HTTPException(
            status_code=500,
            detail=f"Package-Merge error: Generated length exceeds max_length constraint {max_length}."
        )

    # Check Kraft-McMillan inequality
    is_kraft_valid, kraft_sum = check_kraft_inequality(lengths)
    if not is_kraft_valid:
        raise HTTPException(
            status_code=500,
            detail=f"Package-Merge error: Kraft inequality violated: sum(2^-l) = {kraft_sum} > 1.0"
        )

    # 6. Generate canonical prefix codewords
    # Sort symbols primarily by codeword length ascending, secondarily by symbol name
    sym_len_list = [
        (sorted_items[i][0], lengths[i], sorted_items[i][1], sorted_items[i][2])
        for i in range(n)
    ]
    sym_len_list.sort(key=lambda x: (x[1], x[0]))

    codebook_map: Dict[str, str] = {}
    curr_code = 0
    curr_len = 0
    for sym, l, freq, prob in sym_len_list:
        if l > curr_len:
            curr_code <<= (l - curr_len)
            curr_len = l
        codebook_map[sym] = bin(curr_code)[2:].zfill(l)
        curr_code += 1

    # Verify prefix-free property
    valid_pf, pf_msg = is_prefix_free(codebook_map)
    if not valid_pf:
        raise HTTPException(status_code=500, detail=f"Package-Merge prefix violation: {pf_msg}")

    # 7. Construct prefix trie / tree for visualization
    class TrieNode:
        def __init__(self, node_id: str, bit: Optional[str] = None):
            self.node_id = node_id
            self.symbol: Optional[str] = None
            self.weight: float = 0.0
            self.bit = bit
            self.left: Optional['TrieNode'] = None
            self.right: Optional['TrieNode'] = None

    root_trie = TrieNode("pm_root")
    trie_node_id = 1

    # Populate trie
    for sym, freq, prob in normalized_items:
        code = codebook_map[sym]
        curr = root_trie
        curr.weight += freq
        for char in code:
            if char == '0':
                if not curr.left:
                    curr.left = TrieNode(f"pm_node_{trie_node_id}", bit="0")
                    trie_node_id += 1
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = TrieNode(f"pm_node_{trie_node_id}", bit="1")
                    trie_node_id += 1
                curr = curr.right
            curr.weight += freq
        curr.symbol = sym

    def serialize_trie(node: Optional[TrieNode], code: str = "", depth: int = 0) -> Optional[TreeNode]:
        if not node:
            return None
        children = []
        if node.left:
            children.append(serialize_trie(node.left, code + "0", depth + 1))
        if node.right:
            children.append(serialize_trie(node.right, code + "1", depth + 1))

        name = node.symbol if node.symbol else f"Σ={round(node.weight, 2)}"
        return TreeNode(
            id=node.node_id,
            name=name,
            weight=round(node.weight, 2),
            symbol=node.symbol,
            code=code if node.symbol else None,
            bit=node.bit,
            depth=depth,
            children=children if children else None
        )

    tree_model = serialize_trie(root_trie)

    # 8. Compute final metrics
    codebook_entries: List[CodebookEntry] = []
    final_lengths: List[int] = []
    probs: List[float] = []

    for sym, freq, prob in normalized_items:
        cw = codebook_map.get(sym, "")
        l = len(cw)
        final_lengths.append(l)
        probs.append(prob)
        codebook_entries.append(CodebookEntry(
            symbol=sym,
            frequency=freq,
            probability=round(prob, 4),
            codeword=cw,
            length=l,
            register_compatible=(l <= max_length)
        ))

    avg_len = calculate_average_length(probs, final_lengths)
    entropy = calculate_entropy(probs)
    efficiency = round((entropy / avg_len) * 100.0, 2) if avg_len > 0 else 0.0
    redundancy = round(avg_len - entropy, 5)
    comp_ratio = round(fixed_bits / avg_len, 4) if avg_len > 0 else 0.0
    savings_pct = round(((fixed_bits - avg_len) / fixed_bits) * 100.0, 2)
    max_len = max(final_lengths) if final_lengths else 0
    all_compat = all(l <= max_length for l in final_lengths)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return CompressionResponse(
        algorithm=f"Package-Merge (L<={max_length})",
        codebook=codebook_entries,
        codebook_map=codebook_map,
        tree=tree_model,
        average_length=avg_len,
        entropy=entropy,
        efficiency=efficiency,
        redundancy=redundancy,
        compression_ratio=comp_ratio,
        bandwidth_savings_pct=savings_pct,
        kraft_sum=round(kraft_sum, 5),
        max_codeword_length=max_len,
        hardware_compatible=all_compat,
        operations_count=ops_count,
        execution_time_ms=round(elapsed_ms, 3)
    )

def brute_force_optimal_cost(
    normalized_items: List[Tuple[str, float, float]],
    max_length: int = 4
) -> float:
    """
    Brute-force validator for small N (<= 8) to mathematically prove Package-Merge optimality.
    """
    from itertools import product
    weights = [item[1] for item in normalized_items]
    tot = sum(weights)
    n = len(weights)
    if n > 8:
        return -1.0  # Search space too large for brute force

    best_cost = float("inf")
    for lens in product(range(1, max_length + 1), repeat=n):
        if sum(2.0 ** (-l) for l in lens) <= 1.000001:
            cost = sum(w * l for w, l in zip(weights, lens))
            if cost < best_cost:
                best_cost = cost
    return round(best_cost / tot, 5)

