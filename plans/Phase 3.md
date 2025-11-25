# Phase 4: Frontend Core MVP (Flutter App, Basic User Journey)

**Role:**  
You are a coding assistant for a non-technical founder.  
After each step, provide a clear update (did it work, any output/errors, and ask for clarification if blocked).

---

## Step 1. Scaffold Frontend Project

1. Create `/frontend/lib` and `/frontend/test`.
2. Initialize Flutter project, if not already:  
    ```
    flutter create frontend
    ```
    or manually arrange files as needed.
3. Add minimal README to `/frontend`.

**How to validate:**  
- Show directory tree for `/frontend`.

---

## Step 2. Implement Base URL Helper

1. In `/frontend/lib/utils/base_url_helper.dart`, add:
    ```
    import 'dart:io';
    import 'package:flutter/foundation.dart' show kIsWeb;

    class BaseUrlHelper {
      static String getBaseUrl() {
        if (kIsWeb) {
          return 'http://localhost:8000';
        } else if (Platform.isAndroid) {
          return 'http://10.0.2.2:8000';
        } else if (Platform.isIOS || Platform.isMacOS) {
          return 'http://localhost:8000';
        } else if (Platform.isWindows || Platform.isLinux) {
          return 'http://127.0.0.1:8000';
        }
        return 'http://localhost:8000';
      }
    }
    ```

**How to validate:**  
- Show file contents and run a unit test for the helper.

---

## Step 3. Add MVP Screens

1. Create minimal screens (can be stateless widgets with static text initially) in `/frontend/lib/screens`:
    - `onboarding_screen.dart` (headline + CTA button)
    - `registration_screen.dart` (fields: email, password, display name, key toggle, Register button)
    - `login_screen.dart` (fields: email, password, Sign In button)
    - `key_confirmation_screen.dart` (shows current public key, Generate New Key button)
    - `message_send_screen.dart` (recipient dropdown, text area, Send Message button)

**How to validate:**  
- Show navigation flow running locally:
    ```
    flutter run
    ```
- Screenshot or summary of visible screens.

---

## Step 4. Implement API Client Service

1. In `/frontend/lib/services/api_client.dart`, add:
   - Functions for register, login, send message using the BaseUrlHelper for endpoint URLs.
   - Use `http` package.
2. For MVP, just handle JSON request/reply.

**How to validate:**  
- Show code snippets and test registration/login against running backend.  
- Print sample API response to console.

---

## Step 5. Local Dilithium Key Storage (Placeholder MVP)

1. In `/frontend/lib/services/dilithium_service.dart`,  
   - For now, stub out key gen and sign message with dummy base64 strings.
   - Document in README how/when to replace with actual PQC integration.

**How to validate:**  
- Show placeholder public/private key output in UI.

---

## Step 6. Full User Journey Test

1. Run app and confirm workflow:
    - Onboarding → Registration → Key Confirmation → Message Send
2. Use hardcoded recipients for MVP.

**How to validate:**  
- Print success message after sending test message: "Message sent securely"
- Confirm signature verified status displayed

---

## After each step:  
**Report:**
- What was created/changed
- UI/API/client output or errors (or summary)
- Stop and ask for clarification if anything fails or is unclear