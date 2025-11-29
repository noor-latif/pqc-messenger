import 'package:flutter/material.dart';

import 'app_state.dart';
import 'screens/key_confirmation_screen.dart';
import 'screens/login_screen.dart';
import 'screens/message_send_screen.dart';
import 'screens/onboarding_screen.dart';
import 'screens/registration_screen.dart';
import 'services/api_client.dart';
import 'services/dilithium_service.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const PQCMessengerRoot());
}

class PQCMessengerRoot extends StatefulWidget {
  const PQCMessengerRoot({super.key});

  @override
  State<PQCMessengerRoot> createState() => _PQCMessengerRootState();
}

class _PQCMessengerRootState extends State<PQCMessengerRoot> {
  late final AppState _appState;

  @override
  void initState() {
    super.initState();
    _appState = AppState(
      apiClient: ApiClient(),
      dilithiumService: const DilithiumService(),
    );
  }

  @override
  void dispose() {
    _appState.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AppStateProvider(
      notifier: _appState,
      child: MaterialApp(
        title: 'PQC Messenger',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        initialRoute: OnboardingScreen.routeName,
        routes: {
          OnboardingScreen.routeName: (_) => const OnboardingScreen(),
          RegistrationScreen.routeName: (_) => const RegistrationScreen(),
          LoginScreen.routeName: (_) => const LoginScreen(),
          KeyConfirmationScreen.routeName: (_) =>
              const KeyConfirmationScreen(),
          MessageSendScreen.routeName: (_) => const MessageSendScreen(),
        },
      ),
    );
  }
}


