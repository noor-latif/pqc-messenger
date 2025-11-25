# PQC Messenger

Post-quantum secure messenger MVP scaffold with a FastAPI backend, Docker-first workflow, and Flutter client shell.

## Prerequisites
- Docker Desktop (macOS/Windows) or Docker Engine (Linux/WSL2)
- Flutter SDK 3.24.0+ (with Dart)
- Git 2.40+

## One-Command Setup
```bash
git clone https://github.com/your-org/pqc-messenger.git \
  && cd pqc-messenger \
  && cp .env.example .env \
  && docker compose up --build
```
The backend will hot-reload from `backend/app` and expose `http://localhost:8000/api/healthz`. Launch the Flutter shell in a second terminal with:
```bash
cd frontend && flutter run
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

## Docker Notes
- `backend/Dockerfile` uses multi-stage builds on `python:3.13` to compile pinned `liboqs` and `liboqs-python` releases with `uv` for dependency management.
- `docker-compose.yml` mounts `backend/app` for instant reloads and surfaces a `/api/healthz` endpoint used in the health check.

## Troubleshooting
| Symptom | Fix |
| --- | --- |
| `docker compose` fails compiling liboqs | Ensure at least 8 GB RAM is available to Docker and rerun `docker compose build --no-cache`. |
| `curl http://localhost:8000/api/healthz` fails | Confirm the backend container is healthy (`docker ps`), then inspect logs with `docker compose logs backend`. |
| Flutter app cannot reach backend | Verify the BaseUrl helper matches your platform and that ports are forwarded when using emulators or WSL2. |
| CORS errors in browser | Add the browser origin to `.env` `ALLOWED_ORIGINS` and restart `docker compose up`. |

## Contributing
Read `docs/open_source_guide.md` for the branching model, testing expectations, and issue reporting workflow.
