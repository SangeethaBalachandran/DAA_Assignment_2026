import pytest
from ..schemas.compression import EncodeRequest, DecodeRequest
from ..services.compression_service import compression_service
from ..services.codebook_service import codebook_service
from ..api.encoder import encode_messages, decode_bitstream

def test_roundtrip_lossless_encoding():
    messages = ["OK", "TEMP_HI", "OK", "RESET", "DOOR", "FAULT", "HUM", "OK", "VIB", "OK"]
    codebook = compression_service.generate_package_merge().codebook_map

    enc_req = EncodeRequest(messages=messages, codebook_map=codebook)
    enc_resp = encode_messages(enc_req)
    assert enc_resp.message_count == len(messages)
    assert len(enc_resp.encoded_bitstream) == enc_resp.compressed_bits
    assert enc_resp.compressed_bits < enc_resp.original_bits

    dec_req = DecodeRequest(bitstream=enc_resp.encoded_bitstream, codebook_map=codebook)
    dec_resp = decode_bitstream(dec_req)
    assert dec_resp.success is True
    assert dec_resp.decoded_symbols == messages

def test_codebook_version_enforcement():
    messages = ["OK", "FAULT"]
    codebook = codebook_service.get_current_codebook()
    enc_req = EncodeRequest(messages=messages, codebook_map=codebook)
    enc_resp = encode_messages(enc_req)

    # Decode with matching version
    dec_req_valid = DecodeRequest(
        bitstream=enc_resp.encoded_bitstream,
        codebook_map=codebook,
        codebook_version=codebook_service.current_version
    )
    dec_resp_valid = decode_bitstream(dec_req_valid)
    assert dec_resp_valid.success is True

    # Decode with outdated version
    dec_req_invalid = DecodeRequest(
        bitstream=enc_resp.encoded_bitstream,
        codebook_map=codebook,
        codebook_version="v0.9.0"
    )
    with pytest.raises(Exception):
        decode_bitstream(dec_req_invalid)

