from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field

class SymbolFrequency(BaseModel):
    symbol: str
    frequency: float = Field(..., ge=0, description="Observed count or frequency weight")

class CompressionRequest(BaseModel):
    frequencies: List[SymbolFrequency]
    name: Optional[str] = "custom"

class PackageMergeRequest(BaseModel):
    frequencies: List[SymbolFrequency]
    max_length: int = Field(default=4, ge=1, le=16, description="Maximum permitted codeword length in bits")

class CodebookEntry(BaseModel):
    symbol: str
    frequency: float
    probability: float
    codeword: str
    length: int
    register_compatible: bool

class TreeNode(BaseModel):
    id: str
    name: str
    weight: float
    symbol: Optional[str] = None
    code: Optional[str] = None
    bit: Optional[str] = None
    depth: int = 0
    children: Optional[List["TreeNode"]] = None

class CompressionResponse(BaseModel):
    algorithm: str
    codebook: List[CodebookEntry]
    codebook_map: Dict[str, str]
    tree: Optional[TreeNode] = None
    average_length: float
    entropy: float
    efficiency: float
    redundancy: float
    compression_ratio: float
    bandwidth_savings_pct: float
    kraft_sum: float
    max_codeword_length: int
    hardware_compatible: bool
    operations_count: int
    execution_time_ms: float

class TwoQueueStep(BaseModel):
    step_number: int
    q1_before: List[str]
    q2_before: List[str]
    popped: List[str]
    merged_weight: float
    result_node: str
    description: str

class TwoQueueResponse(CompressionResponse):
    steps: List[TwoQueueStep]

class AlgorithmComparisonResponse(BaseModel):
    huffman: CompressionResponse
    shannon_fano: CompressionResponse
    two_queue: CompressionResponse
    is_counterexample: bool
    length_difference: float
    explanation: str

class EncodeRequest(BaseModel):
    messages: List[str]
    codebook_map: Optional[Dict[str, str]] = None
    algorithm: Optional[str] = "huffman"

class EncodeResponse(BaseModel):
    encoded_bitstream: str
    message_count: int
    original_bits: int
    compressed_bits: int
    compression_ratio: float
    bandwidth_saved_pct: float

class DecodeRequest(BaseModel):
    bitstream: str
    codebook_map: Dict[str, str]
    codebook_version: Optional[str] = None

class DecodeResponse(BaseModel):
    decoded_symbols: List[str]
    success: bool
    error: Optional[str] = None
    symbols_decoded: int
    total_bits_consumed: int

