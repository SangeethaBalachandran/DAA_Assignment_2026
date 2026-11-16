import time
import heapq
from typing import List, Tuple, Dict, Optional, Any
from ..schemas.compression import (
    CodebookEntry, TreeNode, CompressionResponse
)
from ..utils.metrics import calculate_entropy, calculate_average_length
from ..utils.validation import check_kraft_inequality, is_prefix_free

class HuffmanNode:
    def __init__(
        self,
        weight: float,
        symbol: Optional[str] = None,
        left: Optional['HuffmanNode'] = None,
        right: Optional['HuffmanNode'] = None,
        tie_breaker: int = 0,
        node_id: str = ""
    ):
        self.weight = weight
        self.symbol = symbol
        self.left = left
        self.right = right
        self.tie_breaker = tie_breaker
        self.node_id = node_id

    def __lt__(self, other: 'HuffmanNode') -> bool:
        if abs(self.weight - other.weight) > 1e-9:
            return self.weight < other.weight
        return self.tie_breaker < other.tie_breaker

def build_huffman_tree(
    normalized_items: List[Tuple[str, float, float]],
    fixed_bits: int = 3
) -> CompressionResponse:
    """
    Constructs an optimal prefix tree using Python heapq min-heap.
    Tracks operations count and execution time.
    """
    start_time = time.perf_counter()
    heap: List[HuffmanNode] = []
    tie_counter = 0
    ops_count = 0

    # 1. Initialize heap with leaf nodes
    for sym, freq, prob in normalized_items:
        node = HuffmanNode(
            weight=freq,
            symbol=sym,
            tie_breaker=tie_counter,
            node_id=f"leaf_{sym}"
        )
        tie_counter += 1
        heapq.heappush(heap, node)
        ops_count += 1

    internal_id = 1
    # 2. Greedy merge
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        ops_count += 2

        parent = HuffmanNode(
            weight=n1.weight + n2.weight,
            symbol=None,
            left=n1,
            right=n2,
            tie_breaker=tie_counter,
            node_id=f"node_{internal_id}"
        )
        internal_id += 1
        tie_counter += 1
        heapq.heappush(heap, parent)
        ops_count += 1

    root = heap[0] if heap else None

    # 3. Traverse tree and assign prefix codewords
    codebook_map: Dict[str, str] = {}

    def extract_codes(node: Optional[HuffmanNode], prefix: str = ""):
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

    # 4. Convert to serializable TreeNode structure
    def serialize_tree(node: Optional[HuffmanNode], code: str = "", bit: Optional[str] = None, depth: int = 0) -> Optional[TreeNode]:
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

    # 5. Calculate statistics and codebook entries
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
        algorithm="Huffman (Min-Heap)",
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

