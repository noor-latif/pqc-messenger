import 'package:flutter/material.dart';

import '../app_state.dart';

class MessageSendScreen extends StatefulWidget {
  const MessageSendScreen({super.key});

  static const routeName = '/message-send';

  @override
  State<MessageSendScreen> createState() => _MessageSendScreenState();
}

class _MessageSendScreenState extends State<MessageSendScreen> {
  final _messageController = TextEditingController();

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateProvider.of(context);
    return AnimatedBuilder(
      animation: appState,
      builder: (context, _) {
        final recipients = appState.recipients;
        final selected = appState.selectedRecipient ?? recipients.first;
        return Scaffold(
          appBar: AppBar(
            title: const Text('Send secure message'),
          ),
          body: LayoutBuilder(
            builder: (context, constraints) => SingleChildScrollView(
              child: ConstrainedBox(
                constraints: BoxConstraints(minHeight: constraints.maxHeight),
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: IntrinsicHeight(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        DropdownButtonFormField<String>(
                          value: selected.id,
                          decoration: const InputDecoration(
                            labelText: 'Recipient',
                          ),
                          items: recipients
                              .map(
                                (recipient) => DropdownMenuItem(
                                  value: recipient.id,
                                  child: Text(recipient.name),
                                ),
                              )
                              .toList(),
                          onChanged: (value) {
                            if (value != null) {
                              appState.selectRecipient(value);
                            }
                          },
                        ),
                        const SizedBox(height: 16),
                        TextField(
                          controller: _messageController,
                          maxLines: 5,
                          decoration: const InputDecoration(
                            labelText: 'Message',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text('Public key id: ${appState.keyId ?? '—'}'),
                        const SizedBox(height: 4),
                        Text(
                          'Signature status: ${appState.lastSignatureStatus ?? 'n/a'}',
                        ),
                        const Spacer(),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton(
                            onPressed: appState.isBusy
                                ? null
                                : () => _sendMessage(appState, context),
                            child: appState.isBusy
                                ? const SizedBox(
                                    width: 18,
                                    height: 18,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                    ),
                                  )
                                : const Text('Send Message'),
                          ),
                        ),
                        if (appState.infoMessage != null) ...[
                          const SizedBox(height: 12),
                          Text(appState.infoMessage!),
                        ],
                        if (appState.errorMessage != null) ...[
                          const SizedBox(height: 12),
                          Text(
                            appState.errorMessage!,
                            style: TextStyle(
                              color: Theme.of(context).colorScheme.error,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  Future<void> _sendMessage(AppState appState, BuildContext context) async {
    final message = _messageController.text.trim();
    if (message.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Message cannot be empty')),
      );
      return;
    }

    final success = await appState.sendMessage(message);
    if (!mounted) {
      return;
    }

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Message sent securely')),
      );
      _messageController.clear();
    } else if (appState.errorMessage != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(appState.errorMessage!)),
      );
    }
  }
}
