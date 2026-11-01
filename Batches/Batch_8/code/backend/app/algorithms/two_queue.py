import time
from collections import deque
from typing import List, Tuple, Dict, Optional, Any
from ..schemas.compression import (
    CodebookEntry, TreeNode, TwoQueueStep, TwoQueueResponse
)
from ..utils.metrics import calculate_entropy, calculate_average_length
from ..utils.validation import check_kraft_inequality

class TQNode:
    def __init__(
        self,
        weight: float,
        symbol: Optional[str] = None,
        left: Optional['TQNode'] = None,
        right: Optional['TQNode'] = None,
        tie_breaker: int = 0,
        node_id: str = ""
    ):
        self.weight = weight
        self.symbol = symbol
        self.left = left
        self.right = right
        self.tie_breaker = tie_breaker
        self.node_id = node_id

def build_two_queue_huffman(
    normalized_items: List[Tuple[str, float, float]],
    fixed_bits: int = 3
) -> TwoQueueResponse:
    """
    Constructs an optimal Huffman tree in linear O(N) time given pre-sorted leaves
    using the Two-Queue algorithm (van Leeuwen, 1976).
    Records detailed step-by-step queue states for visual animation.
    """
    start_time = time.perf_counter()
    ops_count = 0

    # 1. Sort leaf nodes ascending by frequency for Queue 1
    # Note: If input is already sorted, this step is O(1). Otherwise O(N log N).
    sorted_items = sorted(normalized_items, key=lambda x: x[1])
    ops_count += len(sorted_items)

    q1: deque[TQNode] = deque()
    for i, (sym, freq, prob) in enumerate(sorted_items):
        q1.append(TQNode(
            weight=freq,
            symbol=sym,
            tie_breaker=i,
            node_id=f"tq_leaf_{sym}"
        ))

    q2: deque[TQNode] = deque()
    steps: List[TwoQueueStep] = []
    tie_counter = len(sorted_items)
    step_num = 1
    internal_id = 1

    def pop_minimum() -> Tuple[TQNode, str]:
        nonlocal ops_count
        ops_count += 1
        if not q1:
            return q2.popleft(), "Q2"
        if not q2:
            return q1.popleft(), "Q1"

        if q1[0].weight < q2[0].weight:
            return q1.popleft(), "Q1"
        elif q1[0].weight > q2[0].weight:
            return q2.popleft(), "Q2"
        else:
            # Tie breaker: prefer Q1 or lower tie_breaker
            if q1[0].tie_breaker <= q2[0].tie_breaker:
                return q1.popleft(), "Q1"
            else:
                return q2.popleft(), "Q2"

    # Merge until a single root remains
    while (len(q1) + len(q2)) > 1:
        q1_snapshot = [f"{n.symbol or n.node_id} ({round(n.weight, 2)})" for n in q1]
        q2_snapshot = [f"{n.symbol or n.node_id} ({round(n.weight, 2)})" for n in q2]

        n1, src1 = pop_minimum()
        n2, src2 = pop_minimum()

        merged_w = n1.weight + n2.weight
        parent = TQNode(
            weight=merged_w,
            symbol=None,
            left=n1,
            right=n2,
            tie_breaker=tie_counter,
            node_id=f"tq_node_{internal_id}"
        )
        internal_id += 1
        tie_counter += 1
        q2.append(parent)

        desc = (
            f"Step {step_num}: Dequeued {n1.symbol or n1.node_id} ({round(n1.weight, 2)}) from {src1} "
            f"and {n2.symbol or n2.node_id} ({round(n2.weight, 2)}) from {src2}. "
            f"Enqueued new internal node {parent.node_id} ({round(parent.weight, 2)}) into Q2."
        )

        steps.append(TwoQueueStep(
            step_number=step_num,
            q1_before=q1_snapshot,
            q2_before=q2_snapshot,
            popped=[f"{n1.symbol or n1.node_id}:{round(n1.weight, 2)} ({src1})", f"{n2.symbol or n2.node_id}:{round(n2.weight, 2)} ({src2})"],
            merged_weight=round(merged_w, 2),
            result_node=f"{parent.node_id} ({round(parent.weight, 2)})",
            description=desc
        ))
        step_num += 1

    root = q2.popleft() if q2 else (q1.popleft() if q1 else None)

    # Traverse tree and extract prefix codes
    codebook_map: Dict[str, str] = {}

    def extract_codes(node: Optional[TQNode], prefix: str = ""):
        if not node:
            return
        if node.symbol is not None:
            codebook_map[node.symbol] = prefix if prefix else "0"
            return
        if node.left:
            extract_codes(node.left, prefix + "0")
        if node.right:
            extract_codes(node.right, prefix + "1")

    extract_codes(root)

    # Convert to serializable TreeNode
    def serialize_tree(node: Optional[TQNode], code: str = "", bit: Optional[str] = None, depth: int = 0) -> Optional[TreeNode]:
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

    return TwoQueueResponse(
        algorithm="Two-Queue Huffman (O(N))",
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
        execution_time_ms=round(elapsed_ms, 3),
        steps=steps
    )

