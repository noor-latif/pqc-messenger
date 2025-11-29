import 'package:flutter/material.dart';

import 'services/api_client.dart';
import 'services/dilithium_service.dart';

class Recipient {
  const Recipient({required this.id, required this.name});

  final String id;
  final String name;
}

class AppState extends ChangeNotifier {
  AppState({
    required ApiClient apiClient,
    required DilithiumService dilithiumService,
  }) : _apiClient = apiClient,
       _dilithiumService = dilithiumService {
    selectedRecipient = recipients.first;
  }

  final ApiClient _apiClient;
  final DilithiumService _dilithiumService;

  bool isBusy = false;
  String? errorMessage;
  String? infoMessage;
  String? authToken;
  String? keyId;
  String? publicKey;
  String? privateKey;
  String? lastSignatureStatus;
  String? lastMessageId;

  final List<Recipient> recipients = const [
    Recipient(id: 'user-alice', name: 'Alice (Compliance)'),
    Recipient(id: 'user-bob', name: 'Bob (Ops)'),
    Recipient(id: 'user-carol', name: 'Carol (Security)'),
  ];
  Recipient? selectedRecipient;

  void selectRecipient(String recipientId) {
    selectedRecipient = recipients.firstWhere(
      (recipient) => recipient.id == recipientId,
      orElse: () => recipients.first,
    );
    notifyListeners();
  }

  Future<bool> registerUser({
    required String email,
    required String password,
    required String displayName,
    required bool generateOnDevice,
  }) async {
    _setBusy(true);
    errorMessage = null;
    infoMessage = null;
    try {
      final result = await _apiClient.register(
        email: email,
        password: password,
        displayName: displayName,
        generateOnDevice: generateOnDevice,
      );
      authToken = result.authToken;
      if (generateOnDevice) {
        await _hydrateLocalKeypair();
        infoMessage = 'Using locally generated Dilithium key.';
      } else {
        keyId = result.keyId;
        publicKey = result.publicKey;
        privateKey = null;
        infoMessage = 'Server key provisioned.';
      }
      notifyListeners();
      return true;
    } on ApiException catch (error) {
      errorMessage = error.message;
      notifyListeners();
      return false;
    } finally {
      _setBusy(false);
    }
  }

  Future<bool> loginUser({
    required String email,
    required String password,
  }) async {
    _setBusy(true);
    errorMessage = null;
    try {
      final result = await _apiClient.login(email: email, password: password);
      authToken = result.authToken;
      notifyListeners();
      return true;
    } on ApiException catch (error) {
      errorMessage = error.message;
      notifyListeners();
      return false;
    } finally {
      _setBusy(false);
    }
  }

  Future<void> generateNewKeyPair() async {
    await _hydrateLocalKeypair();
    infoMessage = 'Generated a fresh placeholder Dilithium key.';
    notifyListeners();
  }

  Future<bool> sendMessage(String messageBody) async {
    if (authToken == null) {
      errorMessage = 'Please register or login first.';
      notifyListeners();
      return false;
    }

    _setBusy(true);
    errorMessage = null;
    try {
      final recipient = selectedRecipient ?? recipients.first;
      if (keyId == null) {
        // No backend key to reference yet; simulate a local success.
        final signature = await _dilithiumService.signMessage(
          privateKey: privateKey ?? 'placeholder-private',
          message: messageBody,
        );
        lastMessageId = 'local-${DateTime.now().millisecondsSinceEpoch}';
        lastSignatureStatus = 'Local signature issued (not sent to backend)';
        infoMessage =
            'Generated placeholder signature $signature. Configure backend key to send upstream.';
        notifyListeners();
        return true;
      }

      MessageSendResult result;
      if (privateKey == null) {
        result = await _apiClient.sendMessage(
          authToken: authToken!,
          recipientId: recipient.id,
          messageBody: messageBody,
          publicKeyId: keyId!,
        );
        lastSignatureStatus = result.signatureValid
            ? 'Server-side signature verified'
            : 'Server-side signature rejected';
        infoMessage = 'Message signed by server-managed key.';
      } else {
        final signature = await _dilithiumService.signMessage(
          privateKey: privateKey!,
          message: messageBody,
        );
        result = await _apiClient.sendMessage(
          authToken: authToken!,
          recipientId: recipient.id,
          messageBody: messageBody,
          signature: signature,
          publicKeyId: keyId!,
        );
        lastSignatureStatus = result.signatureValid
            ? 'Signature verified'
            : 'Signature rejected';
        infoMessage = 'Message sent securely.';
      }
      lastMessageId = result.messageId;
      notifyListeners();
      return true;
    } on ApiException catch (error) {
      errorMessage = error.message;
      notifyListeners();
      return false;
    } finally {
      _setBusy(false);
    }
  }

  Future<void> _hydrateLocalKeypair() async {
    final pair = await _dilithiumService.generateKeyPair();
    keyId = pair.keyId;
    publicKey = pair.publicKey;
    privateKey = pair.privateKey;
  }

  void clearTransientMessages() {
    errorMessage = null;
    infoMessage = null;
    notifyListeners();
  }

  void _setBusy(bool value) {
    isBusy = value;
    notifyListeners();
  }

  @override
  void dispose() {
    _apiClient.dispose();
    super.dispose();
  }
}

class AppStateProvider extends InheritedNotifier<AppState> {
  const AppStateProvider({
    required AppState notifier,
    required Widget child,
    super.key,
  }) : super(notifier: notifier, child: child);

  static AppState of(BuildContext context) {
    final provider = context
        .dependOnInheritedWidgetOfExactType<AppStateProvider>();
    if (provider == null) {
      throw StateError('AppStateProvider not found in widget tree');
    }
    return provider.notifier!;
  }

  @override
  bool updateShouldNotify(covariant AppStateProvider oldWidget) =>
      notifier != oldWidget.notifier;
}
