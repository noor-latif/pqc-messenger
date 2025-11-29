import 'package:flutter/material.dart';

import '../app_state.dart';
import 'message_send_screen.dart';

class KeyConfirmationScreen extends StatelessWidget {
  const KeyConfirmationScreen({super.key});

  static const routeName = '/key-confirmation';

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    return AnimatedBuilder(
      animation: appState,
      builder: (context, _) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Key confirmation'),
          ),
          body: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Current public key',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    color: Theme.of(context)
                        .colorScheme
                        .surfaceContainerHighest
                        .withOpacity(0.4),
                  ),
                  child: SelectableText(
                    appState.publicKey ?? 'No key available yet.',
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'Key identifier: ${appState.keyId ?? '—'}',
                ),
                if (appState.privateKey != null) ...[
                  const SizedBox(height: 12),
                  Text(
                    'Private key (placeholder)',
                    style: Theme.of(context).textTheme.titleSmall,
                  ),
                  const SizedBox(height: 4),
                  SelectableText(appState.privateKey!),
                ],
                const Spacer(),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: () => appState.generateNewKeyPair(),
                    child: const Text('Generate New Key'),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: FilledButton(
                    onPressed: () {
                      Navigator.pushNamed(context, MessageSendScreen.routeName);
                    },
                    child: const Text('Continue to Messaging'),
                  ),
                ),
                if (appState.infoMessage != null) ...[
                  const SizedBox(height: 12),
                  Text(appState.infoMessage!),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
