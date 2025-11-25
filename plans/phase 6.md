# Phase 6: GitLab CI/CD MVP (Automated Build and Testing Pipeline)

**Role:**  
You are a coding assistant for a non-technical founder.  
After each step, provide a clear update (did it work, any output/errors, and ask for clarification if blocked).

---

## Step 1. Create `.gitlab-ci.yml` in Repository Root

1. Start with these stages:
    ```
    stages:
      - build
      - test-backend
      - test-frontend
    ```
2. Add jobs for:
    - `build:backend` (build Docker image for backend)
    - `test:backend:pytest` (run backend pytest in Docker)
    - `test:backend:ruff` (run ruff lint)
    - `test:backend:black` (run black formatting)
    - `test:frontend` (run flutter tests in Docker)

**How to validate:**  
- Show created `.gitlab-ci.yml`
- Use `gitlab-ci-lint` (in GitLab UI or CLI) to confirm syntax.

---

## Step 2. Backend Build Job

1. Use Docker-in-Docker (`image: docker:24-dind` for build job/service).
2. Build backend image using `/backend/Dockerfile`, cache result, optionally push to container registry if configured.
3. Pass on built image for downstream jobs if possible.

**How to validate:**  
- Paste logs from first build.
- Confirm container artifact is created.

---

## Step 3. Backend Test/Lint Jobs

1. Use built backend image for testing:  
    ```
    test:backend:pytest:
      stage: test-backend
      image: <backend-image>
      script:
        - cd backend
        - pytest --cov=app
    test:backend:ruff:
      ...
    test:backend:black:
      ...
    ```
2. Ensure these jobs run in parallel after build, using the same environment as local dev.

**How to validate:**  
- Screenshot or logs of passing test, ruff, and black jobs.

---

## Step 4. Frontend Test Job (Flutter in Docker)

1. Use Flutter Docker image (`ghcr.io/cirruslabs/flutter:stable`) for frontend test stage.
2. Run:
    ```
    test:frontend:
      stage: test-frontend
      image: ghcr.io/cirruslabs/flutter:stable
      script:
        - cd frontend
        - flutter pub get
        - flutter test --coverage
    ```

**How to validate:**  
- Paste logs and coverage output.
- Confirm test artifacts and reports.

---

## Step 5. Cache and Performance Optimizations (Optional)

1. Add Docker layer caching and dependency cache for faster builds.
2. Make sure jobs only rebuild if files changed.

**How to validate:**  
- Compare first run (slow) vs re-run (fast, hit cache).

---

## Step 6. Add Pipeline Status Badge to README

1. In `README.md` (root), add a badge that shows latest pipeline status:
    ```
    [
    ```

**How to validate:**  
- Verify badge updates after pipeline runs.

---

## Step 7. Troubleshooting and Final Report

- If any job fails, review logs and error details.
- Summarize what succeeded, which tests passed, coverage %, and if any steps await clarification.

---

## After each step:  
**Report:**
- What was created/changed
- Which job ran/passed/failed, and output/logs
- If anything fails or is unclear, stop and ask for next steps