from __future__ import annotations

import sys
import types
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

oqs_stub = types.ModuleType("oqs")


class FakeSignature:
    """Minimal oqs.Signature stand-in for unit tests."""

    def __init__(self, algorithm: str, *_: object) -> None:
        self.algorithm = algorithm
        self._public_key = b"pub-" + algorithm.encode()
        self._secret_key = b"sec-" + algorithm.encode()

    def __enter__(self) -> FakeSignature:
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # pragma: no cover - unused
        return False

    def generate_keypair(self) -> bytes:
        return self._public_key

    def export_secret_key(self) -> bytes:
        return self._secret_key

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        return False


class MechanismNotSupportedError(Exception):
    """Compatibility placeholder for liboqs exceptions."""


def fake_get_enabled_sig_mechanisms() -> tuple[str, ...]:
    return ("Dilithium3",)


oqs_stub.Signature = FakeSignature
oqs_stub.MechanismNotSupportedError = MechanismNotSupportedError
oqs_stub.get_enabled_sig_mechanisms = fake_get_enabled_sig_mechanisms
sys.modules["oqs"] = oqs_stub

from app import storage  # noqa: E402  (import after oqs stub)
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_storage() -> Iterator[None]:
    """Ensure the in-memory storage is clean between tests."""

    storage.users_by_id.clear()
    storage.users_by_email.clear()
    storage.sessions_by_token.clear()
    storage.keys_by_id.clear()
    storage.messages_by_id.clear()
    yield
    storage.users_by_id.clear()
    storage.users_by_email.clear()
    storage.sessions_by_token.clear()
    storage.keys_by_id.clear()
    storage.messages_by_id.clear()


@pytest.fixture
def client() -> Iterator[TestClient]:
    """FastAPI test client fixture shared across modules."""

    with TestClient(app) as test_client:
        yield test_client


