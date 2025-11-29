"""Post-quantum cryptography service wrapper for ML-KEM operations using liboqs."""

import base64
import logging
from functools import lru_cache
from typing import NamedTuple, Optional

import oqs

logger = logging.getLogger(__name__)

# ML-KEM algorithm candidates (Kyber variants)
ML_KEM_CANDIDATES = ("ML-KEM-768", "Kyber768", "ML-KEM-1024", "Kyber1024")


class KeyPair(NamedTuple):
    """Container for public and private key pair."""

    public_key: bytes
    private_key: bytes


class EncapsulationResult(NamedTuple):
    """Container for encapsulated shared secret and ciphertext."""

    shared_secret: bytes
    ciphertext: bytes


@lru_cache(maxsize=1)
def _resolve_kem_algorithm() -> str:
    """Pick the first supported ML-KEM algorithm from candidates."""
    available = set(oqs.get_enabled_kem_mechanisms())
    logger.info(f"Available KEM mechanisms: {sorted(available)}")
    
    for candidate in ML_KEM_CANDIDATES:
        if candidate in available:
            logger.info(f"Selected KEM algorithm: {candidate}")
            return candidate
    
    raise RuntimeError(
        f"No supported ML-KEM implementations found. Available: {sorted(available)}"
    )


def generate_kem_keypair() -> tuple[KeyPair, str]:
    """
    Generate a new ML-KEM key pair.
    
    Returns:
        Tuple of (KeyPair(public_key, private_key), algorithm_name)
    """
    algorithm = _resolve_kem_algorithm()
    
    try:
        with oqs.KeyEncapsulation(algorithm) as kem:
            public_key = kem.generate_keypair()
            private_key = kem.export_secret_key()
            
            logger.debug(
                f"Generated {algorithm} keypair - "
                f"public: {len(public_key)} bytes, private: {len(private_key)} bytes"
            )
            
            return KeyPair(public_key=public_key, private_key=private_key), algorithm
    except Exception as e:
        logger.error(f"Failed to generate {algorithm} keypair: {e}")
        raise RuntimeError(f"Key generation failed: {e}") from e


def encapsulate(public_key: bytes, algorithm: Optional[str] = None) -> EncapsulationResult:
    """
    Encapsulate a shared secret using the recipient's public key.
    
    Args:
        public_key: Recipient's public key bytes
        algorithm: KEM algorithm name (auto-detected if None)
    
    Returns:
        EncapsulationResult(shared_secret, ciphertext)
    """
    if algorithm is None:
        algorithm = _resolve_kem_algorithm()
    
    try:
        with oqs.KeyEncapsulation(algorithm) as kem:
            ciphertext, shared_secret = kem.encap_secret(public_key)
            
            logger.debug(
                f"Encapsulated shared secret using {algorithm} - "
                f"ciphertext: {len(ciphertext)} bytes, secret: {len(shared_secret)} bytes"
            )
            
            return EncapsulationResult(
                shared_secret=shared_secret, ciphertext=ciphertext
            )
    except Exception as e:
        logger.error(f"Failed to encapsulate with {algorithm}: {e}")
        raise RuntimeError(f"Encapsulation failed: {e}") from e


def decapsulate(
    private_key: bytes, ciphertext: bytes, algorithm: Optional[str] = None
) -> bytes:
    """
    Decapsulate a shared secret using the recipient's private key.
    
    Args:
        private_key: Recipient's private key bytes
        ciphertext: Encapsulated ciphertext from sender
        algorithm: KEM algorithm name (auto-detected if None)
    
    Returns:
        Shared secret bytes
    """
    if algorithm is None:
        algorithm = _resolve_kem_algorithm()
    
    try:
        with oqs.KeyEncapsulation(algorithm, private_key) as kem:
            shared_secret = kem.decap_secret(ciphertext)
            
            logger.debug(
                f"Decapsulated shared secret using {algorithm} - "
                f"secret: {len(shared_secret)} bytes"
            )
            
            return shared_secret
    except Exception as e:
        logger.error(f"Failed to decapsulate with {algorithm}: {e}")
        raise RuntimeError(f"Decapsulation failed: {e}") from e


def encode_key_base64(key: bytes) -> str:
    """Encode a key as base64 string."""
    return base64.b64encode(key).decode("ascii")


def decode_key_base64(key_b64: str) -> bytes:
    """Decode a base64-encoded key."""
    return base64.b64decode(key_b64)

