"""Authentication router and business logic for the PQC Messenger API."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext

from app import models
from app.keys import generate_backend_key_for_user
from app.storage import (
    User,
    generate_id,
    generate_token,
    sessions_by_token,
    users_by_email,
    users_by_id,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _serialize_user_profile(user: User) -> models.UserProfile:
    return models.UserProfile(
        user_id=user.user_id,
        email=user.email,
        display_name=user.display_name,
    )


def _issue_auth_token(user_id: str) -> str:
    token = generate_token()
    sessions_by_token[token] = user_id
    return token


def _create_user(
    email: str,
    password_hash: str,
    display_name: str,
) -> User:
    user = User(
        user_id=generate_id(),
        email=email,
        display_name=display_name,
        password_hash=password_hash,
    )
    users_by_id[user.user_id] = user
    users_by_email[email] = user.user_id
    return user


@router.post(
    "/register",
    response_model=models.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: models.RegisterRequest) -> models.RegisterResponse:
    normalized_email = _normalize_email(payload.email)
    if normalized_email in users_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    password_hash = _hash_password(payload.password)
    user = _create_user(
        email=normalized_email,
        password_hash=password_hash,
        display_name=payload.display_name,
    )
    auth_token = _issue_auth_token(user.user_id)

    key_id: Optional[str] = None
    public_key: Optional[str] = None

    if not payload.generate_on_device:
        key_record = generate_backend_key_for_user(user.user_id)
        key_id = key_record.key_id
        public_key = key_record.public_key_b64

    return models.RegisterResponse(
        user_id=user.user_id,
        key_id=key_id,
        public_key=public_key,
        auth_token=auth_token,
    )


@router.post("/login", response_model=models.LoginResponse)
def login(payload: models.LoginRequest) -> models.LoginResponse:
    normalized_email = _normalize_email(payload.email)
    user_id = users_by_email.get(normalized_email)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    user = users_by_id[user_id]
    if not _verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    auth_token = _issue_auth_token(user.user_id)

    return models.LoginResponse(
        auth_token=auth_token,
        user_profile=_serialize_user_profile(user),
    )

