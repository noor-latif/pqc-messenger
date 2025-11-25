"""Message handling router for Dilithium signature verification."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/messages", tags=["Messages"])


@router.get("/__placeholder__")
async def _placeholder() -> dict[str, str]:
    """Temporary placeholder route."""
    return {"status": "pending"}

