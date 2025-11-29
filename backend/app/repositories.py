"""Repository pattern helpers for database operations."""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db_models import User


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    pqc_public_key: Optional[str] = None,
    pqc_private_blob: Optional[str] = None,
) -> User:
    """Create a new user in the database."""
    user = User(
        email=email.lower().strip(),
        password_hash=password_hash,
        pqc_public_key=pqc_public_key,
        pqc_private_blob=pqc_private_blob,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def find_user_by_email(db: Session, email: str) -> Optional[User]:
    """Find a user by email address."""
    return db.query(User).filter(User.email == email.lower().strip()).first()


def find_user_by_id(db: Session, user_id: UUID | str) -> Optional[User]:
    """Find a user by ID."""
    if isinstance(user_id, str):
        try:
            user_id = UUID(user_id)
        except ValueError:
            return None
    return db.query(User).filter(User.id == user_id).first()

