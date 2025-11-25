from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from uuid import uuid4


def generate_id() -> str:
    """Return a random hex string suitable for user/key/message IDs."""
    return uuid4().hex


def generate_token() -> str:
    """Return a random auth token."""
    return uuid4().hex


@dataclass(slots=True)
class User:
    user_id: str
    email: str
    display_name: str
    password_hash: str


@dataclass(slots=True)
class KeyRecord:
    key_id: str
    user_id: str
    public_key_b64: str
    private_key_b64: str | None
    algorithm: str


@dataclass(slots=True)
class MessageRecord:
    message_id: str
    sender_id: str
    recipient_id: str
    message_body: str
    signature_b64: str
    public_key_id: str
    signature_valid: bool
    created_at: datetime


users_by_id: Dict[str, User] = {}
users_by_email: Dict[str, str] = {}
sessions_by_token: Dict[str, str] = {}
keys_by_id: Dict[str, KeyRecord] = {}
messages_by_id: Dict[str, MessageRecord] = {}
