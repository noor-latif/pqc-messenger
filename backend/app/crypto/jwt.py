"""JWT token generation and validation utilities."""

import datetime
from typing import Optional
from uuid import UUID

import jwt

from app.config import get_settings

settings = get_settings()


def create_jwt_token(user_id: UUID | str, redirect: str = "/dashboard") -> str:
    """
    Create a JWT token for a user.
    
    Args:
        user_id: User's unique identifier
        redirect: Redirect path after login (default: /dashboard)
    
    Returns:
        Encoded JWT token string
    """
    now = datetime.datetime.utcnow()
    expiration = now + datetime.timedelta(hours=settings.jwt_expiration_hours)
    
    payload = {
        "sub": str(user_id),  # Subject (user ID)
        "exp": expiration,
        "iat": now,
        "redirect": redirect,
    }
    
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    
    return token


def decode_jwt_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dictionary or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

