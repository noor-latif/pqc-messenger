"""Tests for /auth/login endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crypto.password import hash_password
from app.db_models import User
from app.database import Base, SessionLocal, engine, get_db
from app.main import app
from app.repositories import create_user


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session):
    """Create test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session):
    """Create a test user in the database."""
    password_hash = hash_password("TestPassword123!")
    user = create_user(
        db_session,
        email="test@example.com",
        password_hash=password_hash,
    )
    return user


def test_login_success(client: TestClient, test_user: User):
    """Test successful login returns JWT token and redirect."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["redirect"] == "/dashboard"
    assert len(data["token"]) > 0


def test_login_invalid_email(client: TestClient, test_user: User):
    """Test login with invalid email returns 401."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "TestPassword123!",
        },
    )
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_login_invalid_password(client: TestClient, test_user: User):
    """Test login with invalid password returns 401."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword",
        },
    )
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_login_missing_fields(client: TestClient):
    """Test login with missing fields returns validation error."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
        },
    )
    
    assert response.status_code == 422  # Validation error

