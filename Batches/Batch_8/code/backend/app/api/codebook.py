from fastapi import APIRouter
from ..schemas.telemetry import (
    CodebookBroadcastRequest, CodebookBroadcastResponse
)
from ..services.codebook_service import codebook_service

router = APIRouter(prefix="/api/codebook", tags=["Gateway Codebook Management"])

@router.get("/current")
def get_current_codebook():
    """
    Returns the currently deployed codebook version and mapping table.
    """
    return {
        "version": codebook_service.current_version,
        "codebook": codebook_service.get_current_codebook(),
        "total_receivers": len(codebook_service.receiver_table)
    }

@router.post("/broadcast", response_model=CodebookBroadcastResponse)
def broadcast_codebook(req: CodebookBroadcastRequest):
    """
    Simulates broadcasting an updated codebook to all 5,000 receivers.
    Models ACK replies, retries, and network overhead.
    """
    return codebook_service.broadcast_codebook(req)

@router.get("/history")
def get_broadcast_history():
    return {
        "current_version": codebook_service.current_version,
        "history": codebook_service.version_history
    }

