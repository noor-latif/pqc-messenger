# Phase 5: Frontend Tests MVP (Widget, Form, and Integration Tests)

**Role:**  
You are a coding assistant for a non-technical founder.  
After each step, provide a clear update (did it work, any output/errors, and ask for clarification if blocked).

---

## Step 1. Prepare Test Dependencies

1. In `/frontend/pubspec.yaml`, add dev dependencies:
    ```
    dev_dependencies:
      flutter_test:
        sdk: flutter
      flutter_lints: ^3.0.0
      mockito: ^5.4.4
      build_runner: ^2.4.7
      integration_test:
        sdk: flutter
    ```

**How to validate:**  
- Run `flutter pub get` and report any dependency errors.

---

## Step 2. Write Widget Tests (Per Screen)

1. In `/frontend/test/screens`, create test files:
    - `onboarding_screen_test.dart`
    - `registration_screen_test.dart`
    - `login_screen_test.dart`
    - `key_confirmation_screen_test.dart`
    - `message_send_screen_test.dart`
2. For each, write tests for:
    - Rendering key elements (text, buttons, inputs)
    - Correct validation errors (invalid email, short password)
    - Navigation between screens

**How to validate:**  
- Run:
    ```
    flutter test test/screens/
    ```
- Show output summary (tests run, passed, failed).

---

## Step 3. Mock API Client and Storage

1. In `/frontend/test/mocks`, add mock classes for:
    - API client (register, login, send message)
    - Storage (for key persistence)
2. Use them in integration and widget tests to simulate different backend scenarios.

**How to validate:**  
- Demo test with mock returning dummy user/key.

---

## Step 4. Integration Test for Full User Journey

1. In `/frontend/test/integration/user_journey_test.dart`:
    - Simulate onboarding → registration → key confirmation → send message
    - Use only mocks (no network/downstream errors)
    - Assert correct state and output after each step

**How to validate:**  
- Run:
    ```
    flutter test test/integration/
    ```
- Output: journey completes with success message/verified chip

---

## Step 5. Gather Coverage Data

1. Run all tests with coverage:
    ```
    flutter test --coverage
    ```
2. Optionally generate HTML report:
    ```
    genhtml coverage/lcov.info -o coverage/html
    open coverage/html/index.html
    ```

**How to validate:**  
- Share coverage % and any missing branches.

---

## After each step:  
**Report:**
- Which tests were written, # passing/failing, coverage info
- Any errors or flakes, and ask for clarification if test fails without apparent reason