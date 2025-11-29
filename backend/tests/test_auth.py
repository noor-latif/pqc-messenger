from __future__ import annotations

from fastapi.testclient import TestClient


def test_register_and_login_flow(client: TestClient) -> None:
    register_payload = {
        "email": "alice@example.com",
        "password": "pass1234",
        "display_name": "Alice",
    }
    register_resp = client.post("/api/auth/register", json=register_payload)
    assert register_resp.status_code == 201
    register_data = register_resp.json()
    assert register_data["user_id"]
    assert register_data["auth_token"]
    assert register_data["key_id"]
    assert register_data["public_key"]

    login_resp = client.post(
        "/api/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["auth_token"]
    assert login_data["user_profile"]["user_id"] == register_data["user_id"]


def test_duplicate_email_rejected(client: TestClient) -> None:
    payload = {
        "email": "duplicate@example.com",
        "password": "pass1234",
        "display_name": "Dupe",
    }
    first_resp = client.post("/api/auth/register", json=payload)
    assert first_resp.status_code == 201

    second_resp = client.post("/api/auth/register", json=payload)
    assert second_resp.status_code == 409
    assert second_resp.json()["detail"] == "A user with this email already exists."



