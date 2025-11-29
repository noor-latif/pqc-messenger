"""FastAPI application entrypoint with health check endpoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.config import get_settings
from app.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="PQC Messenger API",
    version="0.1.0",
    description="Post-quantum secure messenger API with ML-KEM and Argon2id",
    lifespan=lifespan,
)

allowed_origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)


@app.get("/api/healthz", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Simple readiness probe used by Docker and infrastructure monitors."""
    return {"status": "ok"}

