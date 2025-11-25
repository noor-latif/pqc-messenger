# PQC Messenger Open Source Guide

Welcome! This document captures expectations for anyone collaborating on the PQC Messenger project.

## Code of Conduct Principles
- Be respectful and inclusive of contributors from all backgrounds.
- Assume good intent; ask clarifying questions when unsure.
- Provide constructive, actionable review feedback.
- Avoid sharing sensitive or proprietary data in issues or PRs.

## How to Contribute
1. **Fork** the repository to your account.
2. **Create a feature branch** using GitFlow-style naming (e.g., `feature/health-endpoint`).
3. **Make focused changes**, keeping commits small and descriptive.
4. **Test locally** (Docker + Flutter) before opening a PR.
5. **Open a pull request** against `main`, describing the motivation, approach, and validation steps.
6. **Respond to reviews** promptly and keep discussions public for transparency.

## Development Setup
- Install Docker (Desktop on macOS/Windows, Engine on Linux/WSL2).
- Install Flutter 3.24.0+ and the matching Dart SDK.
- Clone the repo, copy `.env.example` to `.env`, then run `docker compose up --build` to start the backend.
- Launch the Flutter app with `flutter run` (desktop, mobile, or web) pointing to the backend base URL helper.

## Testing Expectations
- Backend changes require unit tests (pytest + httpx) and lint checks (ruff, black).
- Frontend changes require widget or integration tests via `flutter test`.
- Document new manual verification steps in PR descriptions.

## Code Style
- **Backend**: Format with `black`, lint with `ruff`, prefer type hints and FastAPI dependency injection patterns.
- **Frontend**: Follow Flutter's `flutter_lints` defaults, embrace Material 3 widgets, and keep BaseUrl logic centralized.
- Keep files small and cohesive; favor composition over inheritance.

## Issue Reporting
- Use GitHub issues to track bugs or feature requests.
- Provide reproduction steps, expected vs. actual behavior, and environment details (OS, Docker/Flutter versions).
- Tag issues with appropriate labels (e.g., `bug`, `enhancement`, `docs`).

Thanks for contributing to PQC Messenger!
