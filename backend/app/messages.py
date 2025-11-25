"""Message handling router for Dilithium signature verification."""

from __future__ import annotations

import base64
import binascii
from datetime import datetime, timezone

import oqs
from fastapi import APIRouter, HTTPException, status

from app import models
from app.keys import require_user
from app.storage import (
    MessageRecord,
    generate_id,
    keys_by_id,
    messages_by_id,
)

router = APIRouter(prefix="/api/messages", tags=["Messages"])


def _b64_decode(value: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except binascii.Error as exc:  # pragma: no cover - defensive.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value must be valid base64.",
        ) from exc


@router.post(
    "/send",
    response_model=models.MessageSendResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(payload: models.MessageSendRequest) -> models.MessageSendResponse:
    sender = require_user(payload.auth_token)

    key_record = keys_by_id.get(payload.public_key_id)
    if not key_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unknown public_key_id.",
        )

    public_key_bytes = _b64_decode(key_record.public_key_b64)
    signature_bytes = _b64_decode(payload.signature)
    message_bytes = payload.message_body.encode("utf-8")

    try:
        with oqs.Signature(key_record.algorithm) as verifier:
            signature_valid = bool(
                verifier.verify(message_bytes, signature_bytes, public_key_bytes)
            )
    except oqs.MechanismNotSupportedError as exc:  # pragma: no cover - env specific.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signature algorithm {key_record.algorithm} is not supported.",
        ) from exc

    message_id = generate_id()
    messages_by_id[message_id] = MessageRecord(
        message_id=message_id,
        sender_id=sender.user_id,
        recipient_id=payload.recipient_id,
        message_body=payload.message_body,
        signature_b64=payload.signature,
        public_key_id=payload.public_key_id,
        signature_valid=signature_valid,
        created_at=datetime.now(tz=timezone.utc),
    )

    return models.MessageSendResponse(
        message_id=message_id,
        signature_valid=signature_valid,
    )
