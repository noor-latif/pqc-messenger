"""Key management router for Dilithium/ML-DSA operations."""

from __future__ import annotations

import base64
from functools import lru_cache

import oqs
from fastapi import APIRouter, HTTPException, status

from app import models
from app.storage import (
    KeyRecord,
    User,
    generate_id,
    keys_by_id,
    sessions_by_token,
    users_by_id,
)

router = APIRouter(prefix="/api/keys", tags=["Keys"])

SIGNATURE_ALGORITHM_CANDIDATES = ("Dilithium3", "ML-DSA-65")


def _b64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


@lru_cache(maxsize=1)
def _resolve_signature_algorithm() -> str:
    """Pick the first supported algorithm from our candidate list."""
    available = set(oqs.get_enabled_sig_mechanisms())
    for candidate in SIGNATURE_ALGORITHM_CANDIDATES:
        if candidate in available:
            return candidate
    raise RuntimeError("No supported Dilithium/ML-DSA implementations were found in liboqs.")


def require_user(auth_token: str) -> User:
    """Resolve the user for an auth token or raise HTTP 401."""
    user_id = sessions_by_token.get(auth_token)
    if not user_id or user_id not in users_by_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired auth token.",
        )
    return users_by_id[user_id]


def generate_backend_key_for_user(user_id: str) -> KeyRecord:
    """Generate and persist a signature keypair for the given user."""
    try:
        algorithm = _resolve_signature_algorithm()
    except RuntimeError as exc:  # pragma: no cover - environment-specific
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    with oqs.Signature(algorithm) as signer:
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()

    key_record = KeyRecord(
        key_id=generate_id(),
        user_id=user_id,
        public_key_b64=_b64_encode(public_key),
        private_key_b64=_b64_encode(secret_key),
        algorithm=algorithm,
    )
    keys_by_id[key_record.key_id] = key_record
    return key_record


@router.post(
    "/generate",
    response_model=models.KeyGenerateResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_key(payload: models.KeyGenerateRequest) -> models.KeyGenerateResponse:
    user = require_user(payload.auth_token)

    if payload.generate_on_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="generate_on_device=true indicates client-side key generation.",
        )

    key_record = generate_backend_key_for_user(user.user_id)
    return models.KeyGenerateResponse(
        key_id=key_record.key_id,
        public_key=key_record.public_key_b64,
    )
