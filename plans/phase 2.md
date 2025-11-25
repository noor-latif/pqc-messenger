# Phase 2: Backend Core MVP Endpoints & Key Logic

**Role:**  
You are a coding assistant for a non-technical founder.  
After each step, provide a clear update: did it work, any output/errors, and ask for clarification if blocked.

---

## Step 1. Prep Basic Backend File Structure

1. In `/backend/app`, create:
    - `main.py` (already exists from Phase 1)
    - `models.py` (for Pydantic schemas)
    - `auth.py` (for registration/login logic)
    - `keys.py` (for Dilithium key generation)
    - `messages.py` (for message send/verification)

**How to validate:**  
- Show resulting `/backend/app` files with `ls backend/app`.

---

## Step 2. Implement Registration Endpoint

1. Add `POST /api/auth/register` to the FastAPI app.  
    - Request: `{ email, password, display_name, generate_on_device }`
    - Response: `{ user_id, key_id, public_key, auth_token }`
    - Hash password with bcrypt (or passlib)
    - If `generate_on_device: false`, generate Dilithium keypair using `liboqs-python`
2. Store user and key info in an in-memory dict (for MVP).

**How to validate:**  
- Curl example:
    ```
    curl -X POST -H "Content-Type: application/json" \
    -d '{"email":"alice@example.com","password":"pass1234","display_name":"Alice","generate_on_device":false}' \
    http://localhost:8000/api/auth/register
    ```
- Show JSON response.

---

## Step 3. Implement Login Endpoint

1. Add `POST /api/auth/login` to FastAPI app.
    - Request: `{ email, password }`
    - Response: `{ auth_token, user_profile }`
    - Validate credentials and return token.

**How to validate:**  
- Curl example:
    ```
    curl -X POST -H "Content-Type: application/json" \
    -d '{"email":"alice@example.com","password":"pass1234"}' \
    http://localhost:8000/api/auth/login
    ```
- Show JSON response.

---

## Step 4. Implement Key Generation Endpoint

1. Add `POST /api/keys/generate` to FastAPI app.
    - Request: `{ auth_token, generate_on_device }`
    - Response: `{ key_id, public_key }`
    - Use `liboqs-python` Dilithium key generation in backend if `generate_on_device` is false.

**How to validate:**  
- Curl with auth token:
    ```
    curl -X POST -H "Content-Type: application/json" \
    -d '{"auth_token":"...","generate_on_device":false}' \
    http://localhost:8000/api/keys/generate
    ```
- Show JSON response.

---

## Step 5. Implement Message Send/Verify Endpoint

1. Add `POST /api/messages/send` to FastAPI app.
    - Request: `{ auth_token, recipient_id, message_body, signature, public_key_id }`
    - Verify signature with Dilithium3 (using public key from key_id)
    - Response: `{ message_id, signature_valid }`
    - Store each message in-memory for MVP.

**How to validate:**  
- Curl with all fields (use fake signature for smoke test):
    ```
    curl -X POST -H "Content-Type: application/json" \
    -d '{"auth_token":"...","recipient_id":"...", "message_body":"Hello", "signature":"...", "public_key_id":"..."}' \
    http://localhost:8000/api/messages/send
    ```
- Show JSON response with `signature_valid`.

---

## Step 6. Confirm Health Endpoint Still Works

- `GET /api/healthz` must still return `{ "status":"ok" }`.

**How to validate:**  
- Curl health URL:
    ```
    curl http://localhost:8000/api/healthz
    ```
- Show output.

---

## After each step:
**Report:**
- What was created/changed
- The output or error (or summary)
- If anything is unclear or fails, stop and ask for clarification.
