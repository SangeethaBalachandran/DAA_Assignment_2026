from fastapi import APIRouter
from typing import Optional
from ..schemas.compression import CompressionRequest, CompressionResponse
from ..services.compression_service import compression_service

router = APIRouter(prefix="/api/huffman", tags=["Huffman Engine"])

@router.get("/default", response_model=CompressionResponse)
def get_default_huffman():
    """
    Returns the standard min-heap Huffman codebook and binary tree
    for the exact 8-symbol industrial IoT telemetry distribution.
    """
    return compression_service.generate_huffman()

@router.post("/generate", response_model=CompressionResponse)
def generate_huffman(req: CompressionRequest):
    """
    Constructs an optimal Huffman tree and codebook for custom frequencies.
    """
    return compression_service.generate_huffman(req.frequencies)

