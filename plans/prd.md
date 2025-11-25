**Product Requirements Document: Post-Quantum Secure Messaging Demo App**

**Context:**  
Demo project aiming to showcase secure messaging using post-quantum digital signatures (ML-DSA/Dilithium).  
Target audience: Junior test infrastructure engineer, including GitLab CI/CD for automated testing and project management via GitLab CLI.

***

**Core Features**
- **Flutter Mobile Frontend**
  - UI for registration, login, and messaging
  - Visual explanation of post-quantum signature operations
- **Python Backend (FastAPI/Flask)**
  - REST API for key management (Dilithium signature keypairs), signing, verification, and basic message routing

***

**Cryptographic Operations (PQC)**
- **Keypair Generation**
  - Using ML-DSA (use python libraries)
  - Each user generates their signature keypair on device or requests backend generation
- **Message Signing and Verification**
  - Message sent is signed with user’s private ML-DSA key
  - Recipient verifies message using sender’s public key via backend
- **Demo: Show "quantum-resistant" workflow and technical steps in UI**

***

**Infrastructure & Automation**
- **GitLab Repository**
  - Project initialized and managed via GitLab CLI (`glab`)
- **CI/CD Pipeline (GitLab CI)**
  - `.gitlab-ci.yml` for automated linting and testing
  - Test jobs for:
    - `test:backend` — Python tests covering Dilithium signer/verifier endpoints
    - `test:frontend` — Flutter widget tests for messaging flow
    - `lint:backend`, `lint:frontend` — style checks for Python/Dart

***

**Project Setup Steps (Sample)**
1. **Repo Structure:**
    - `/backend/` (Python FastAPI, PQC libraries for ML-DSA)
    - `/frontend/` (Flutter)
    - `.gitlab-ci.yml` (root)
2. **Backend Requirements Example:**
    - Use [dilithium-py](https://github.com/GiacomoPope/dilithium-py) using CRYSTALS-Dilithium because it's newer than NIST Module-Lattice-Based Digital Signature Standard
    - API endpoints for Dilithium signing and verification
3. **Sample CI Jobs:**
    ```yaml
    test:backend:
      script:
        - cd backend
        - pytest
    ```
    - Add similar jobs for linting and Flutter testing

***

**User Stories**
- As a user, I can register and generate a Dilithium keypair.
- I can send a signed message to another user, and the app shows signature verification.
- As a test engineer, I see all code changes validated via GitLab CI jobs after each push.
- As a developer I can view the OpenAPI/Swagger UI easily.

***

**Extra/Optional**
- Show educational info about quantum-resistant crypto for junior engineers.

***

**Scope & Constraints**
- The app is for demo and learning; does not require production-grade security or deployment.
- Dilithium operations should use well-maintained, public Python libraries. Use my installed exa mcp to identify best up to date practices.
