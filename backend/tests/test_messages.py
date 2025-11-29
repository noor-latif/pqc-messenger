from __future__ import annotations

import base64

from fastapi.testclient import TestClient


def _register_user(client: TestClient) -> dict:
    resp = client.post(
        "/api/auth/register",
        json={
            "email": "messenger@example.com",
            "password": "pass1234",
            "display_name": "Msg Sender",
        },
    )
    assert resp.status_code == 201
    return resp.json()


def test_message_send_success(client: TestClient) -> None:
    user = _register_user(client)
    fake_signature = base64.b64encode(b"fake-sig").decode()

    resp = client.post(
        "/api/messages/send",
        json={
            "auth_token": user["auth_token"],
            "recipient_id": "recipient-123",
            "message_body": "Hello PQC",
            "signature": fake_signature,
            "public_key_id": user["key_id"],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["message_id"]
    assert body["signature_valid"] is False


def test_message_send_unknown_key(client: TestClient) -> None:
    user = _register_user(client)
    fake_signature = base64.b64encode(b"fake-sig").decode()

    resp = client.post(
        "/api/messages/send",
        json={
            "auth_token": user["auth_token"],
            "recipient_id": "recipient-123",
            "message_body": "Hello PQC",
            "signature": fake_signature,
            "public_key_id": "missing-key",
        },
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Unknown public_key_id."



