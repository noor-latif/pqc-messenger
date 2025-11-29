import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../utils/base_url_helper.dart';

class ApiException implements Exception {
  ApiException(this.message, {this.statusCode});

  final String message;
  final int? statusCode;

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class ApiClient {
  ApiClient({http.Client? httpClient, String? baseUrl})
    : _httpClient = httpClient ?? http.Client(),
      _baseUrl = baseUrl ?? BaseUrlHelper.getBaseUrl();

  final http.Client _httpClient;
  final String _baseUrl;

  Uri _buildUri(String path) => Uri.parse('$_baseUrl$path');

  Future<RegisterResult> register({
    required String email,
    required String password,
    required String displayName,
    required bool generateOnDevice,
  }) async {
    final payload = {
      'email': email,
      'password': password,
      'display_name': displayName,
      'generate_on_device': generateOnDevice,
    };
    final json = await _postJson('/api/auth/register', payload);
    return RegisterResult.fromJson(json);
  }

  Future<LoginResult> login({
    required String email,
    required String password,
  }) async {
    final payload = {'email': email, 'password': password};
    final json = await _postJson('/api/auth/login', payload);
    return LoginResult.fromJson(json);
  }

  Future<MessageSendResult> sendMessage({
    required String authToken,
    required String recipientId,
    required String messageBody,
    String? signature,
    required String publicKeyId,
  }) async {
    final payload = {
      'auth_token': authToken,
      'recipient_id': recipientId,
      'message_body': messageBody,
      'public_key_id': publicKeyId,
    };
    if (signature != null) {
      payload['signature'] = signature;
    }
    final json = await _postJson('/api/messages/send', payload);
    return MessageSendResult.fromJson(json);
  }

  Future<Map<String, dynamic>> _postJson(
    String path,
    Map<String, dynamic> payload,
  ) async {
    try {
      final response = await _httpClient
          .post(
            _buildUri(path),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(payload),
          )
          .timeout(const Duration(seconds: 10));
      debugPrint(
        '[API] POST $path -> ${response.statusCode}: ${response.body}',
      );
      if (response.statusCode >= 200 && response.statusCode < 300) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }

      final detail = _tryExtractDetail(response.body);
      throw ApiException(
        detail ?? 'Request failed with status ${response.statusCode}',
        statusCode: response.statusCode,
      );
    } on SocketException catch (error) {
      throw ApiException('Network error: ${error.message}');
    } on TimeoutException {
      throw ApiException('Request timed out. Is the backend running?');
    }
  }

  String? _tryExtractDetail(String body) {
    try {
      final json = jsonDecode(body);
      if (json is Map<String, dynamic>) {
        final detail = json['detail'];
        if (detail is String) {
          return detail;
        }
      }
    } catch (_) {
      // Ignore JSON parse failures here.
    }
    return null;
  }

  void dispose() {
    _httpClient.close();
  }
}

class RegisterResult {
  RegisterResult({
    required this.userId,
    required this.authToken,
    this.keyId,
    this.publicKey,
  });

  factory RegisterResult.fromJson(Map<String, dynamic> json) => RegisterResult(
    userId: json['user_id'] as String,
    authToken: json['auth_token'] as String,
    keyId: json['key_id'] as String?,
    publicKey: json['public_key'] as String?,
  );

  final String userId;
  final String authToken;
  final String? keyId;
  final String? publicKey;
}

class LoginResult {
  LoginResult({required this.token, required this.redirect});

  factory LoginResult.fromJson(Map<String, dynamic> json) => LoginResult(
    token: json['token'] as String,
    redirect: json['redirect'] as String? ?? '/dashboard',
  );

  final String token;
  final String redirect;
}

class MessageSendResult {
  MessageSendResult({required this.messageId, required this.signatureValid});

  factory MessageSendResult.fromJson(Map<String, dynamic> json) =>
      MessageSendResult(
        messageId: json['message_id'] as String,
        signatureValid: json['signature_valid'] as bool,
      );

  final String messageId;
  final bool signatureValid;
}
