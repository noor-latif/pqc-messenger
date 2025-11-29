"""Tests for PQC (ML-KEM) wrapper service."""

import pytest

from app.crypto.pqc import (
    decapsulate,
    encapsulate,
    generate_kem_keypair,
)


def test_generate_kem_keypair():
    """Test ML-KEM keypair generation."""
    keypair, algorithm = generate_kem_keypair()
    
    assert keypair.public_key is not None
    assert keypair.private_key is not None
    assert len(keypair.public_key) > 0
    assert len(keypair.private_key) > 0
    assert algorithm is not None


def test_encapsulate_decapsulate_roundtrip():
    """Test that encapsulation and decapsulation produce the same shared secret."""
    keypair, algorithm = generate_kem_keypair()
    
    # Encapsulate using public key
    enc_result = encapsulate(keypair.public_key, algorithm)
    
    assert enc_result.shared_secret is not None
    assert enc_result.ciphertext is not None
    assert len(enc_result.shared_secret) > 0
    assert len(enc_result.ciphertext) > 0
    
    # Decapsulate using private key
    shared_secret_dec = decapsulate(
        keypair.private_key,
        enc_result.ciphertext,
        algorithm,
    )
    
    # Shared secrets should match
    assert shared_secret_dec == enc_result.shared_secret


def test_key_encoding():
    """Test base64 encoding/decoding of keys."""
    from app.crypto.pqc import decode_key_base64, encode_key_base64
    
    keypair, _ = generate_kem_keypair()
    
    # Encode and decode public key
    encoded = encode_key_base64(keypair.public_key)
    decoded = decode_key_base64(encoded)
    
    assert decoded == keypair.public_key
    
    # Encode and decode private key
    encoded_private = encode_key_base64(keypair.private_key)
    decoded_private = decode_key_base64(encoded_private)
    
    assert decoded_private == keypair.private_key


