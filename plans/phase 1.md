# Phase 1: Repository Scaffold & Backend Healthcheck (MVP Core)

**Role:**  
You are a coding assistant for a non-technical founder building an MVP.  
After each step, provide a clear update: did it work, any output/errors, and ask for clarification if blocked.

---

## Step 1. Create Repository Structure

1. Create these folders at the repo root:
    - /backend
    - /frontend
    - /docs
2. Add a `.gitignore` to exclude Python, Flutter, Docker, and typical editor artifacts.

**How to validate:**  
- Run `tree -L 2 .` and show the output.

---

## Step 2. Backend: Minimal FastAPI Healthcheck

1. In `/backend/app/main.py`, write a FastAPI app that implements `GET /api/healthz` returning `{ "status": "ok" }`.
2. Add minimal `requirements.txt` with `fastapi` and `uvicorn`.
3. (Optional) Test locally:
    ```
    pip install fastapi uvicorn
    python -m uvicorn app.main:app
    ```
   Visit/curl `localhost:8000/api/healthz`.

**How to validate:**  
- Show example output of `curl http://localhost:8000/api/healthz` (should be JSON with status ok).

---

## Step 3. Multi-stage Dockerfile for Backend

1. In `/backend/Dockerfile`, create a multi-stage Dockerfile:
    - **Builder stage:**
        - `FROM python:3.11-slim AS builder`
        - Install build essentials: `apt-get install -y build-essential cmake git`
        - Clone OQS:
          `git clone --branch 0.9.0 --depth 1 https://github.com/open-quantum-safe/liboqs-python.git`
        - Build and install:
          ```
          cd liboqs-python
          pip install .
          ```
    - **Runtime Stage:**
        - `FROM python:3.11-slim`
        - Copy installed liboqs from builder.
        - Install runtime backend:
          `pip install fastapi uvicorn`
        - Copy `/app` folder.
        - `CMD` should start uvicorn to serve main.py.

**How to validate:**  
- Build image:
  `docker build -t pqc-backend .`
- Show output of `docker run -p 8000:8000 pqc-backend` and `curl http://localhost:8000/api/healthz`.

---

## Step 4. Docker Compose Orchestration

1. Place a `docker-compose.yml` at the repo root:
    ```
    version: '3.9'
    services:
      backend:
        build: ./backend
        ports:
          - "8000:8000"
    ```
2. How to validate:
    - Run `docker compose up --build`
    - Wait for logs to show server ready.
    - Run: `curl http://localhost:8000/api/healthz`
    - Confirm you get `{ "status":"ok" }`

---

## Step 5. Minimal README

1. Add a brief `README.md` with:
    - Project name & description (one sentence)
    - Quickstart:
        ```
        1. git clone ...
        2. docker compose up --build
        3. Visit http://localhost:8000/api/healthz  (expects { "status":"ok" })
        ```
    - TODO list for features _not_ yet implemented.

**How to validate:**  
- Copy/paste README contents.

---

## After each step:  
**Report:**
- What was created/changed
- The exact output or error (or a summary)
- If anything fails or is unclear, stop, and ask for next instruction/clarification.
