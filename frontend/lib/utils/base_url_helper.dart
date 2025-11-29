import 'dart:io';

import 'package:flutter/foundation.dart' show kIsWeb;

/// Thin abstraction that surfaces `dart:io` platform flags in a testable form.
abstract class PlatformInfo {
  const PlatformInfo();

  bool get isAndroid;
  bool get isIOS;
  bool get isMacOS;
  bool get isWindows;
  bool get isLinux;
}

/// Default implementation that proxies the real runtime platform flags.
class SystemPlatformInfo extends PlatformInfo {
  const SystemPlatformInfo();

  @override
  bool get isAndroid => Platform.isAndroid;

  @override
  bool get isIOS => Platform.isIOS;

  @override
  bool get isMacOS => Platform.isMacOS;

  @override
  bool get isWindows => Platform.isWindows;

  @override
  bool get isLinux => Platform.isLinux;
}

/// Resolves the correct backend base URL for every supported platform.
class BaseUrlHelper {
  static const String _fallback = 'http://localhost:8000';

  static String getBaseUrl({
    PlatformInfo platform = const SystemPlatformInfo(),
    bool? isWebOverride,
  }) {
    final bool isWeb = isWebOverride ?? kIsWeb;

    if (isWeb) {
      return _fallback;
    }

    if (platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    }

    if (platform.isIOS || platform.isMacOS) {
      return 'http://localhost:8000';
    }

    if (platform.isWindows || platform.isLinux) {
      return 'http://127.0.0.1:8000';
    }

    return _fallback;
  }
}


