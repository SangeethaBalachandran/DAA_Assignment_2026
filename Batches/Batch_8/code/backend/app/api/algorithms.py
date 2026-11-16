from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from ..schemas.compression import (
    CompressionRequest, PackageMergeRequest, CompressionResponse,
    TwoQueueResponse, AlgorithmComparisonResponse
)
from ..services.compression_service import compression_service
from ..services.benchmark_service import benchmark_service

router = APIRouter(prefix="/api", tags=["Algorithm Laboratory"])

@router.post("/shannon-fano/generate", response_model=CompressionResponse)
def generate_shannon_fano(req: CompressionRequest):
    """
    Constructs a Shannon-Fano codebook using recursive top-down bipartitioning.
    """
    return compression_service.generate_shannon_fano(req.frequencies)

@router.post("/huffman/two-queue", response_model=TwoQueueResponse)
def generate_two_queue(req: CompressionRequest):
    """
    Executes the Two-Queue linear-time O(N) Huffman algorithm (van Leeuwen, 1976),
    returning all intermediate queue states for visualization.
    """
    return compression_service.generate_two_queue(req.frequencies)

@router.post("/package-merge/generate", response_model=CompressionResponse)
def generate_package_merge(req: PackageMergeRequest):
    """
    Executes the Package-Merge algorithm (Larmore & Hirschberg, 1990)
    for length-limited prefix coding with constraint l_i <= max_length.
    """
    return compression_service.generate_package_merge(
        frequencies=req.frequencies,
        max_length=req.max_length
    )

@router.post("/algorithms/compare", response_model=AlgorithmComparisonResponse)
def compare_algorithms(req: CompressionRequest):
    """
    Compares Huffman, Shannon-Fano, and Two-Queue algorithms side-by-side.
    Identifies whether the input distribution constitutes a strict counterexample.
    """
    return compression_service.compare_algorithms(req.frequencies)

@router.get("/algorithms/counterexample")
def get_counterexample(variant: str = Query(default="8-symbol", pattern="^(5-symbol|8-symbol)$")):
    """
    Loads mathematically validated counterexample distributions where
    Shannon-Fano yields strictly higher average code length than Huffman.
    """
    dist = compression_service.get_counterexample_distribution(variant=variant)
    comparison = compression_service.compare_algorithms(dist)
    return {
        "variant": variant,
        "distribution": [item.model_dump() for item in dist],
        "comparison": comparison.model_dump()
    }

@router.get("/algorithms/benchmark")
def get_real_benchmarks():
    """
    Executes real empirical benchmarks comparing Min-Heap vs Two-Queue
    execution times and operations across increasing alphabet sizes.
    """
    return benchmark_service.run_benchmark([8, 32, 128, 512, 1024])
