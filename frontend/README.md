## PQC Messenger Frontend (Flutter)

This package hosts the Flutter MVP that walks a user through onboarding, account registration, Dilithium key confirmation, and message sending against the PQC Messenger backend.

### Project Layout

- `lib/main.dart` – MaterialApp + navigation glue
- `lib/app_state.dart` – lightweight ChangeNotifier that stores auth/session data
- `lib/screens/` – onboarding → registration → key confirmation → message send
- `lib/services/api_client.dart` – HTTP client for register/login/message endpoints
- `lib/services/dilithium_service.dart` – placeholder key generation/signing
- `lib/utils/base_url_helper.dart` – platform-aware backend URL resolution
- `test/` – Flutter unit/widget tests

### Getting Started

1. Install Flutter (`>=3.24.0 <4.0.0`) and run `flutter doctor`.
2. Install dependencies with:
   ```bash
   cd frontend
   flutter pub get
   ```
3. Launch the app:
   ```bash
   flutter run
   ```
4. Target platform-specific builds as needed:
   - Windows desktop:
     ```bash
     flutter run -d windows
     ```
   - Web (Chrome or Edge):
     ```bash
     flutter run -d chrome
     ```

### Testing

Run unit tests (e.g., BaseUrlHelper coverage) with:
```bash
flutter test
```

### PQC Integration Notes

- The placeholder Dilithium flow emits deterministic base64 strings and never leaves the device. Replace `DilithiumService` with the actual PQC client once the cryptography team ships it.
- When a production key manager is in place, wire its outputs into `AppState.registerUser`, `AppState.generateNewKeyPair`, and `AppState.sendMessage`.
- Update the README after replacing the stub so future contributors understand the security posture.

