"""Pydantic models for authentication endpoints."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request payload."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=256)


class LoginResponse(BaseModel):
    """Login response payload with JWT token and redirect path."""

    token: str
    redirect: str = "/dashboard"


