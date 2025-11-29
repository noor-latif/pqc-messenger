# PQC Messenger

Post-quantum secure messenger MVP scaffold with a FastAPI backend, Docker-first workflow, and Flutter client shell.

## Prerequisites
- Docker Desktop (macOS/Windows) or Docker Engine (Linux/WSL2)
- Python 3.9+ with `python-on-whales` package (install with `pip install python-on-whales` or `uv pip install python-on-whales`)
- Flutter SDK 3.24.0+ (with Dart)
- Git 2.40+

## One-Command Setup
```bash
git clone https://gitlab.com/noorlatif/pqc-messenger.git \
  && cd pqc-messenger \
  && cp .env.example .env \
  && python build.py --start
```
The build script will automatically check for and build the base image if needed, then build and start the backend. The backend will hot-reload from `backend/app` and expose `http://localhost:8000/api/healthz`. Launch the Flutter shell in a second terminal with:
```bash
cd frontend && flutter run
```

Subsequent backend runs:
```bash
docker compose up
```

Or use the build script:
```bash
python build.py --start
```

## Directory Overview
```
backend/   # FastAPI app + Dockerfile
frontend/  # Flutter shell with BaseUrl helper
docs/      # Contribution guide and future specs
```

## Backend Configuration
- `.env.example` lists safe defaults for `ALLOWED_ORIGINS`, `ENVIRONMENT`, and `LOG_LEVEL`.
- Update `.env` to whitelist additional origins by providing a comma-separated list (no wildcards). Example:
  `ALLOWED_ORIGINS=http://localhost:8000,http://example.dev:8080`
- The FastAPI app loads settings via `app.config.Settings` and enforces the CORS whitelist via middleware.

## Base URL Helper (Flutter)
`frontend/lib/utils/base_url_helper.dart` resolves the correct backend URL per platform:
- Web & iOS/macOS → `http://localhost:8000`
- Android emulator → `http://10.0.2.2:8000`
- Windows/Linux desktop → `http://127.0.0.1:8000`
- Fallback → `http://localhost:8000`

Within the sample `main.dart`, the helper displays the URL being used so developers can verify connectivity quickly.

## Phase 1 Implementation Status

This project implements Phase 1 of the PQC WhatsApp PoC plan with:
- **Backend**: FastAPI with SQLAlchemy (SQLite), Argon2id password hashing, JWT authentication, ML-KEM (Kyber) via liboqs v0.12.0
- **Frontend**: Flutter login screen with blue accent (#1976D2), JWT token storage, dashboard navigation
- **Authentication**: `/api/auth/login` endpoint that validates credentials, performs ML-KEM handshake, and issues JWT tokens

### PQC Decisions (Phase 1)
- **Password Hashing**: Argon2id via `argon2-cffi` for quantum-resistant password storage
- **Key Exchange**: ML-KEM-768/1024 (Kyber) via liboqs v0.12.0 for post-quantum key encapsulation
- **JWT Signing**: HS256 with configurable secret key (enhanced with ML-KEM shared secret in production)

### Running Tests

**Backend tests:**
```bash
cd backend
docker compose run --rm backend pytest
```

**Frontend tests:**
```bash
cd frontend
flutter test
```

## Docker Notes
- The build process uses a two-stage approach:
  - **Base image** (`pqc-messenger-base:0.12.0`): Contains pre-built `liboqs` and `liboqs-python` wheel. Built once and reused.
  - **Application image**: FastAPI backend using the base image. Rebuilds quickly when app code changes.
- The `build.py` script automatically checks for and builds the base image if missing. This might take a few minutes when run for the first time.
- The build pins `liboqs` `0.12.0` and `liboqs-python` `0.12.0` for Phase 1. Override by setting environment variables when running `build.py`:
  ```bash
  LIBOQS_REF=0.12.0 LIBOQS_PYTHON_REF=0.12.0 python build.py
  ```
- `docker-compose.yml` mounts `backend/app` for instant reloads and surfaces a `/api/healthz` endpoint used in the health check.
- **Alternative build methods**:
  - Direct Python script: `python build.py` (builds without starting) or `python build.py --start` (builds and starts)
  - Manual Docker Compose: `docker compose build` and `docker compose up` (requires base image to exist first)

## Troubleshooting
| Symptom | Fix |
| --- | --- |
| `docker compose` fails compiling liboqs | Ensure at least 8 GB RAM is available to Docker and rerun `docker compose build --no-cache`. |
| `curl http://localhost:8000/api/healthz` fails | Confirm the backend container is healthy (`docker ps`), then inspect logs with `docker compose logs backend`. |
| Flutter app cannot reach backend | Verify the BaseUrl helper matches your platform and that ports are forwarded when using emulators or WSL2. |
| CORS errors in browser | Add the browser origin to `.env` `ALLOWED_ORIGINS` and restart `docker compose up`. |

## Contributing
Read `docs/open_source_guide.md` for the branching model, testing expectations, and issue reporting workflow.
