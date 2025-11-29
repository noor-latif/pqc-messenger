import 'package:flutter/material.dart';

import '../utils/base_url_helper.dart';
import 'login_screen.dart';
import 'registration_screen.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  static const routeName = '/';

  @override
  Widget build(BuildContext context) {
    final baseUrl = BaseUrlHelper.getBaseUrl();
    return Scaffold(
      appBar: AppBar(
        title: const Text('PQC Messenger'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Post-Quantum Secure Messaging',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 12),
            Text(
              'Experience the minimal MVP flow: register, confirm keys, and send a message with Dilithium signatures.',
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 24),
            Text(
              'Backend: $baseUrl',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 32),
            FilledButton(
              onPressed: () {
                Navigator.pushNamed(context, RegistrationScreen.routeName);
              },
              child: const Text('Get Started'),
            ),
            const SizedBox(height: 12),
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, LoginScreen.routeName);
              },
              child: const Text('Already registered? Sign in'),
            ),
          ],
        ),
      ),
    );
  }
}


