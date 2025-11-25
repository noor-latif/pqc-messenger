from __future__ import annotations

from fastapi.testclient import TestClient


def test_allowed_origin_receives_cors_headers(client: TestClient) -> None:
    origin = "http://localhost:8000"
    resp = client.get("/api/healthz", headers={"Origin": origin})
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == origin


def test_blocked_origin_has_no_cors_headers(client: TestClient) -> None:
    resp = client.get("/api/healthz", headers={"Origin": "http://evil.example"})
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") is None


