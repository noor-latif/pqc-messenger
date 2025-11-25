"""Key management router for Dilithium operations."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/keys", tags=["Keys"])


@router.get("/__placeholder__")
async def _placeholder() -> dict[str, str]:
    """Temporary placeholder route."""
    return {"status": "pending"}

