# PQC Messenger MVP Plan (Docker-First, 2025 Best Practices)

## Instruction Confirmation

- Build the MVP (registration, login, Dilithium key generation, basic message send) with identical user journey, API payloads, and white/#27AE60 style. Modernize tooling to Docker-first architecture, multi-stage builds compiling liboqs/liboqs-python, CORS enabled, and GitLab CI using the same images. No new features beyond MVP scope.

## Scope & Constraints

- Backend (FastAPI + `liboqs-python`) runs entirely inside Docker using a multi-stage `backend/Dockerfile` that compiles pinned liboqs/liboqs-python. Dev/prod parity via `docker-compose.yml`.
- Frontend Flutter app runs natively but talks to backend through a single base-URL helper that handles desktop/mobile/web/emulators (`http://localhost:8000`, `http://10.0.2.2:8000`, `http://host.docker.internal:8000`).
- Local setup: `git clone`, `docker compose up --build`, `flutter run`. Works identically on Linux/macOS/Windows/WSL2.
- CORS middleware enables all origins for MVP.
- GitLab CI/CD uses the same Docker images (built once, cached) for lint/test; no host Python/Flutter installs.
- Proceed autonomously, do git commits and auto-approve PR, and provide brief updates after completing each major step.

## MVP User Journey

1. Launch → onboarding “Quantum-resistant security in your pocket” with CTA `Get Started`.
2. Registration → placeholders `Enter your email`, `Create a password`, `Choose a display name`, toggle `Generate key locally`; `Register` calls `POST /api/auth/register`.
3. Login → placeholders `email@example.com`, `Password (min 8 chars)`; `Sign In` hits `POST /api/auth/login`.
4. Key confirmation → card `Your Dilithium Public Key` + `Generate New Keypair` button (green #27AE60).
5. Message send → choose recipient (static), compose sample “Hello, this is a test message”, tap `Send Message`; app signs locally and calls `POST /api/messages/send`, showing `Message sent securely`.

## API Contracts (unchanged)

- `POST /api/auth/register`: `{ "email": "alice@example.com", "password": "P@ssw0rd!", "display_name": "Alice", "generate_on_device": true }` → `{ "user_id": "usr_123", "key_id": "key_456", "public_key": "dilithium_pub_base64", "auth_token": "token123" }`
- `POST /api/auth/login`: `{ "email": "alice@example.com", "password": "P@ssw0rd!" }` → `{ "auth_token": "token123", "user_profile": { "display_name": "Alice" } }`
- `POST /api/keys/generate`: `{ "auth_token": "token123", "generate_on_device": false }` → `{ "key_id": "key_456", "public_key": "dilithium_pub_base64" }`
- `POST /api/messages/send`: `{ "auth_token": "token123", "recipient_id": "usr_789", "message_body": "Hello, this is a test message", "signature": "sig_base64", "public_key_id": "key_456" }` → `{ "message_id": "msg_001", "signature_valid": true }`
- `GET /api/healthz`: simple JSON `{ "status": "ok" }`.

## Frontend Content & Style (unchanged)

- Clean white UI, green (#27AE60) buttons `Register`, `Sign In`, `Send Message`.
- Placeholders and sample message text exactly as previously defined.
- Status chip `Signature Verified` after successful send.
- Base URL helper ensures emulator/desktop/mobile talk to Docker backend seamlessly.

## Architecture Upgrades

- **Docker Compose**: Root `docker-compose.yml` orchestrates `backend` (FastAPI) and optional `db`/`redis` placeholders (if needed later) but for MVP just backend. Exposes port 8000, mounts local volume for hot reload in dev, uses env file for secrets.
- **Backend Dockerfile**: Multi-stage (builder installs deps, compiles liboqs/liboqs-python at pinned versions, final stage w/ slim Python + app). Includes uv install, adds FastAPI app, runs `uvicorn`. Enables CORS middleware in FastAPI startup.
- **CI/CD**: GitLab pipeline builds/pushes backend image once, reuses it for backend tests, builds Flutter docker image (with Flutter SDK) for frontend lint/test so runners do not install SDK manually.
- **Networking**: Document base URL helper in Flutter (detect platform/emulator) and configure CORS to allow host/emulator origins.

## Execution Steps & Docker-Aware Success Criteria

1. **scaffold-repo**

- Deliverables: `/backend`, `/frontend`, `.gitignore`, README (with one-command setup), `docs/open_source_guide.md`, `docker-compose.yml`, backend multi-stage `Dockerfile`, `.env.example`.
- Success: After `git clone` and `docker compose up --build`, backend container starts `uvicorn` on port 8000, serving `/api/healthz`. README explains base URL helper and Flutter run instructions.

2. **backend-core-mvp**

- Implement FastAPI app within Docker image: auth, key generation, message send endpoints; Dilithium service uses compiled liboqs; add CORS middleware allowing typical origins; expose OpenAPI docs.
- Success: With containers running, executing `curl http://localhost:8000/api/auth/register` (per contract) succeeds; keypair generation and message send flows return expected JSON with `signature_valid true`.

3. **backend-tests-mvp**

- Add pytest suite (in `backend/tests/`) plus ruff/black configs. Tests run via `docker compose run --rm backend pytest` to ensure containerized execution.
- Success: `docker compose run --rm backend pytest` and `docker compose run --rm backend ruff check .` both exit 0, proving deterministic Dilithium mocks and lint compliance.

4. **frontend-core-mvp**

- Flutter app uses base URL helper to talk to backend container; screens for onboarding, registration/login, key confirmation, message composer; local key storage.
- Success: With backend container running, running `flutter run` (mobile/web/desktop) allows a user to complete the MVP flow and displays `Message sent securely`. App works on Linux/macOS/Windows/WSL2 thanks to base URL helper and CORS.

5. **frontend-tests-mvp**

- Widget/integration tests verifying form validation, placeholder text, and message send routine with mocked API client.
- Success: `flutter test` passes locally and in CI using the Flutter Docker image.

6. **gitlab-ci-mvp**

- `.gitlab-ci.yml` builds backend Docker image (using same Dockerfile), runs backend tests inside container, reuses artifact or registry cache. Separate job pulls Flutter Docker image to run `flutter test`. No system Python/Flutter install on runners.
- Success: Pipeline completes with cached Docker layers; logs show backend/frontend tests running inside containers identical to local dev.

## Deferred Future Work

- Inbox retrieval, richer verification UI, contact management, educational walkthrough screens/docs will be scoped in later prompts once MVP is solid.

## Implementation Todos

- `scaffold-repo`
- `backend-core-mvp`
- `backend-tests-mvp`
- `frontend-core-mvp`
- `frontend-tests-mvp`
- `gitlab-ci-mvp`