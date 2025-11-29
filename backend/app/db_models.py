"""SQLAlchemy database models for the PQC Messenger application."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, TypeDecorator

from app.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type for SQLite compatibility."""

    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class User(Base):
    """User model with Argon2id password hash and PQC key storage."""

    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    pqc_public_key = Column(Text, nullable=True)
    pqc_private_blob = Column(Text, nullable=True)  # Encrypted private key
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

