from fastapi import APIRouter, HTTPException
from ..schemas.compression import (
    EncodeRequest, EncodeResponse, DecodeRequest, DecodeResponse
)
from ..services.compression_service import compression_service
from ..services.codebook_service import codebook_service

router = APIRouter(prefix="/api/encoder", tags=["Message Encoder & Decoder"])

@router.post("/encode", response_model=EncodeResponse)
def encode_messages(req: EncodeRequest):
    """
    Encodes a sequence of industrial telemetry status symbols into a compressed bitstream.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided for encoding.")

    # Use provided codebook or generate from active algorithm
    codebook = req.codebook_map
    if not codebook:
        if req.algorithm == "package_merge":
            resp = compression_service.generate_package_merge()
        else:
            resp = compression_service.generate_huffman()
        codebook = resp.codebook_map

    bitstream_parts = []
    for msg in req.messages:
        sym = msg.strip()
        if sym not in codebook:
            raise HTTPException(
                status_code=400,
                detail=f"Symbol '{sym}' not found in active codebook: {list(codebook.keys())}"
            )
        bitstream_parts.append(codebook[sym])

    encoded = "".join(bitstream_parts)
    orig_bits = len(req.messages) * 3
    comp_bits = len(encoded)
    cr = round(orig_bits / comp_bits, 4) if comp_bits > 0 else 0.0
    saved_pct = round(((orig_bits - comp_bits) / orig_bits) * 100.0, 2) if orig_bits > 0 else 0.0

    return EncodeResponse(
        encoded_bitstream=encoded,
        message_count=len(req.messages),
        original_bits=orig_bits,
        compressed_bits=comp_bits,
        compression_ratio=cr,
        bandwidth_saved_pct=saved_pct
    )

@router.post("/decode", response_model=DecodeResponse)
def decode_bitstream(req: DecodeRequest):
    """
    Decodes a compressed binary bitstream back into original industrial status symbols.
    Enforces codebook version compatibility if provided.
    """
    if not req.bitstream:
        raise HTTPException(status_code=400, detail="Empty bitstream provided.")

    # Check version match if provided
    if req.codebook_version:
        is_valid_ver, ver_msg = codebook_service.verify_version(req.codebook_version)
        if not is_valid_ver:
            raise HTTPException(status_code=409, detail=ver_msg)

    # Invert codebook for prefix parsing
    inv_map = {code: sym for sym, code in req.codebook_map.items()}

    decoded = []
    buffer = ""
    bits_consumed = 0

    for bit in req.bitstream:
        if bit not in ('0', '1'):
            raise HTTPException(status_code=400, detail=f"Invalid binary character '{bit}' in bitstream.")
        buffer += bit
        bits_consumed += 1
        if buffer in inv_map:
            decoded.append(inv_map[buffer])
            buffer = ""

    if buffer:
        return DecodeResponse(
            decoded_symbols=decoded,
            success=False,
            error=f"Bitstream ended with unparsed trailing bits '{buffer}'. Possible corrupted stream or mismatched codebook.",
            symbols_decoded=len(decoded),
            total_bits_consumed=bits_consumed
        )

    return DecodeResponse(
        decoded_symbols=decoded,
        success=True,
        symbols_decoded=len(decoded),
        total_bits_consumed=bits_consumed
    )

