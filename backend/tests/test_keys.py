from __future__ import annotations

from fastapi.testclient import TestClient


def _register_user(client: TestClient, *, email: str = "keyer@example.com") -> dict:
    resp = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "pass1234",
            "display_name": "Key Tester",
        },
    )
    assert resp.status_code == 201
    return resp.json()


def test_generate_key_success(client: TestClient) -> None:
    user = _register_user(client)

    key_resp = client.post(
        "/api/keys/generate",
        json={"auth_token": user["auth_token"], "generate_on_device": False},
    )
    assert key_resp.status_code == 201
    body = key_resp.json()
    assert body["key_id"]
    assert body["public_key"]


def test_generate_key_requires_valid_token(client: TestClient) -> None:
    _register_user(client)

    resp = client.post(
        "/api/keys/generate",
        json={"auth_token": "invalid-token", "generate_on_device": False},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid or expired auth token."



