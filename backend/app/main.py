from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.config import DEFAULT_ALLOWED_ORIGINS, get_settings
from app.keys import router as keys_router
from app.messages import router as messages_router

settings = get_settings()

app = FastAPI(title="PQC Messenger API", version="0.1.0")

allowed_origins = settings.allowed_origins or DEFAULT_ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(keys_router)
app.include_router(messages_router)


@app.get("/api/healthz", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Simple readiness probe used by Docker and infrastructure monitors."""
    return {"status": "ok"}
