import 'dart:io';

import 'package:flutter/foundation.dart' show kIsWeb;

/// Resolves the correct backend base URL for every supported platform.
class BaseUrlHelper {
  static const String _fallback = 'http://localhost:8000';

  static String getBaseUrl() {
    if (kIsWeb) {
      return _fallback;
    }

    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    }

    if (Platform.isIOS || Platform.isMacOS) {
      return 'http://localhost:8000';
    }

    if (Platform.isWindows || Platform.isLinux) {
      return 'http://127.0.0.1:8000';
    }

    return _fallback;
  }
}


