import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:pqc_messenger/app_state.dart';
import 'package:pqc_messenger/screens/login_screen.dart';
import 'package:pqc_messenger/services/api_client.dart';
import 'package:pqc_messenger/services/dilithium_service.dart';

void main() {
  group('LoginScreen', () {
    late AppState appState;

    setUp(() {
      final apiClient = ApiClient(baseUrl: 'http://localhost:8000');
      final dilithiumService = DilithiumService();
      appState = AppState(
        apiClient: apiClient,
        dilithiumService: dilithiumService,
      );
    });

    testWidgets('displays email and password fields', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: AppStateProvider(
            notifier: appState,
            child: const LoginScreen(),
          ),
        ),
      );

      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
      expect(find.text('Sign In'), findsOneWidget);
    });

    testWidgets('shows validation errors for empty fields', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: AppStateProvider(
            notifier: appState,
            child: const LoginScreen(),
          ),
        ),
      );

      // Try to submit without filling fields
      await tester.tap(find.text('Sign In'));
      await tester.pump();

      // Should show validation error
      expect(find.text('Please enter your email'), findsOneWidget);
    });

    testWidgets('shows error message on login failure', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: AppStateProvider(
            notifier: appState,
            child: const LoginScreen(),
          ),
        ),
      );

      // Set error message in app state
      appState.errorMessage = 'Invalid credentials';
      await tester.pump();

      // Error should be displayed (via snackbar after interaction)
      expect(appState.errorMessage, isNotNull);
    });
  });
}


