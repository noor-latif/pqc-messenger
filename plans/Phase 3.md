# Phase 3: Backend Tests MVP (Pytest, Code Quality, Validation)

**Role:**  
You are a coding assistant for a non-technical founder.  
After each step, provide a clear update (did it work, any output/errors, and ask for clarification if blocked).

---

## Step 1. Prepare Dev Requirements

1. In `/backend/requirements-dev.txt`, add:
    ```
    pytest
    pytest-asyncio
    httpx
    ruff
    black
    ```

**How to validate:**  
- Show contents of `requirements-dev.txt`.

---

## Step 2. Add Test Directory & Fixtures

1. In `/backend/tests`, create:
    - `__init__.py`
    - `conftest.py` with FastAPI test client fixture and reset in-memory data.

**How to validate:**  
- `ls backend/tests` should show the test files.

---

## Step 3. Write Endpoint Unit Tests

1. Create test modules:
    - `test_auth.py` (register/login scenarios)
    - `test_keys.py` (key generation)
    - `test_messages.py` (send/verify message)
    - `test_healthz.py` (health endpoint)
2. Each test should use the FastAPI test client and cover expected success, typical edge cases, and validation failures.

**How to validate:**  
- Run all tests:
    ```
    docker compose run --rm backend pytest
    ```
- Show test run summary (number passed, failed, coverage).

---

## Step 4. Add Code Quality Checks

1. Add `pyproject.toml` at `/backend` with Ruff and Black formatting/linting settings.
2. Run inside Docker:
    ```
    docker compose run --rm backend ruff check .
    docker compose run --rm backend black --check .
    ```

**How to validate:**  
- Paste output/results (should report “no errors found” if all is well).

---

## Step 5. Validate CORS Whitelist Enforcement

1. In `test_cors.py`, cover:
    - Allowed origin succeeds (access-control-allow-origin present & correct).
    - Disallowed origin fails (no CORS response).

**How to validate:**  
- Paste example test code and output/results from test run.

---

## Step 6. Reporting and Troubleshooting

- After running tests, report:
    - Number of tests, coverage %, passing/failing status
    - Any errors or ambiguous behaviors needing clarification

---

## After each step:  
**Report:**
- What was created/changed
- Test output, lint/format results, or error details
- Stop and ask for clarification if anything fails or seems unclear

---

Ready for Phase 4?
