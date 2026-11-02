import time
from typing import List, Tuple, Dict, Optional
from ..schemas.compression import (
    CodebookEntry, TreeNode, CompressionResponse
)
from ..utils.metrics import calculate_entropy, calculate_average_length
from ..utils.validation import check_kraft_inequality

class SFInternalNode:
    def __init__(self, weight: float, symbol: Optional[str] = None, node_id: str = ""):
        self.weight = weight
        self.symbol = symbol
        self.node_id = node_id
        self.left: Optional['SFInternalNode'] = None
        self.right: Optional['SFInternalNode'] = None

def build_shannon_fano(
    normalized_items: List[Tuple[str, float, float]],
    fixed_bits: int = 3
) -> CompressionResponse:
    """
    Constructs a Shannon-Fano code tree top-down by recursive bipartitioning.
    """
    start_time = time.perf_counter()
    ops_count = 0

    # Sort descending by frequency
    sorted_items = sorted(normalized_items, key=lambda x: x[1], reverse=True)
    ops_count += len(sorted_items)

    codebook_map: Dict[str, str] = {sym: "" for sym, _, _ in normalized_items}
    node_counter = 1

    def recursive_partition(items: List[Tuple[str, float, float]], prefix: str = "") -> Optional[SFInternalNode]:
        nonlocal node_counter, ops_count
        if not items:
            return None

        total_weight = sum(item[1] for item in items)
        if len(items) == 1:
            sym, freq, prob = items[0]
            codebook_map[sym] = prefix if prefix else "0"
            return SFInternalNode(weight=freq, symbol=sym, node_id=f"sf_leaf_{sym}")

        # Find best split point
        running = 0.0
        best_diff = float("inf")
        best_split = 1

        for i in range(len(items) - 1):
            running += items[i][1]
            diff = abs(running - (total_weight - running))
            ops_count += 1
            if diff < best_diff:
                best_diff = diff
                best_split = i + 1

        parent = SFInternalNode(weight=total_weight, symbol=None, node_id=f"sf_node_{node_counter}")
        node_counter += 1

        left_items = items[:best_split]
        right_items = items[best_split:]

        parent.left = recursive_partition(left_items, prefix + "0")
        parent.right = recursive_partition(right_items, prefix + "1")
        return parent

    root = recursive_partition(sorted_items)

    # Convert to serializable TreeNode
    def serialize_tree(node: Optional[SFInternalNode], code: str = "", bit: Optional[str] = None, depth: int = 0) -> Optional[TreeNode]:
        if not node:
            return None
        children = []
        if node.left:
            children.append(serialize_tree(node.left, code + "0", "0", depth + 1))
        if node.right:
            children.append(serialize_tree(node.right, code + "1", "1", depth + 1))

        name = node.symbol if node.symbol else f"Σ={round(node.weight, 2)}"
        return TreeNode(
            id=node.node_id,
            name=name,
            weight=round(node.weight, 2),
            symbol=node.symbol,
            code=code if node.symbol else None,
            bit=bit,
            depth=depth,
            children=children if children else None
        )

    tree_model = serialize_tree(root)

    codebook_entries: List[CodebookEntry] = []
    lengths: List[int] = []
    probs: List[float] = []

    for sym, freq, prob in normalized_items:
        cw = codebook_map.get(sym, "")
        l = len(cw)
        lengths.append(l)
        probs.append(prob)
        codebook_entries.append(CodebookEntry(
            symbol=sym,
            frequency=freq,
            probability=round(prob, 4),
            codeword=cw,
            length=l,
            register_compatible=(l <= 4)
        ))

    avg_len = calculate_average_length(probs, lengths)
    entropy = calculate_entropy(probs)
    efficiency = round((entropy / avg_len) * 100.0, 2) if avg_len > 0 else 0.0
    redundancy = round(avg_len - entropy, 5)
    comp_ratio = round(fixed_bits / avg_len, 4) if avg_len > 0 else 0.0
    savings_pct = round(((fixed_bits - avg_len) / fixed_bits) * 100.0, 2)
    _, kraft_val = check_kraft_inequality(lengths)
    max_len = max(lengths) if lengths else 0
    all_compat = all(l <= 4 for l in lengths)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return CompressionResponse(
        algorithm="Shannon-Fano",
        codebook=codebook_entries,
        codebook_map=codebook_map,
        tree=tree_model,
        average_length=avg_len,
        entropy=entropy,
        efficiency=efficiency,
        redundancy=redundancy,
        compression_ratio=comp_ratio,
        bandwidth_savings_pct=savings_pct,
        kraft_sum=round(kraft_val, 5),
        max_codeword_length=max_len,
        hardware_compatible=all_compat,
        operations_count=ops_count,
        execution_time_ms=round(elapsed_ms, 3)
    )

