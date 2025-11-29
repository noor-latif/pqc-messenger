import 'package:flutter_test/flutter_test.dart';
import 'package:pqc_messenger/utils/base_url_helper.dart';

class _FakePlatform extends PlatformInfo {
  const _FakePlatform({
    this.android = false,
    this.ios = false,
    this.macOS = false,
    this.windows = false,
    this.linux = false,
  });

  final bool android;
  final bool ios;
  final bool macOS;
  final bool windows;
  final bool linux;

  @override
  bool get isAndroid => android;

  @override
  bool get isIOS => ios;

  @override
  bool get isMacOS => macOS;

  @override
  bool get isWindows => windows;

  @override
  bool get isLinux => linux;
}

void main() {
  group('BaseUrlHelper.getBaseUrl', () {
    test('returns localhost for web builds', () {
      expect(
        BaseUrlHelper.getBaseUrl(isWebOverride: true),
        'http://localhost:8000',
      );
    });

    test('returns Android emulator loopback', () {
      const platform = _FakePlatform(android: true);
      expect(
        BaseUrlHelper.getBaseUrl(platform: platform),
        'http://10.0.2.2:8000',
      );
    });

    test('returns localhost for iOS', () {
      const platform = _FakePlatform(ios: true);
      expect(
        BaseUrlHelper.getBaseUrl(platform: platform),
        'http://localhost:8000',
      );
    });

    test('returns localhost for macOS', () {
      const platform = _FakePlatform(macOS: true);
      expect(
        BaseUrlHelper.getBaseUrl(platform: platform),
        'http://localhost:8000',
      );
    });

    test('returns 127.0.0.1 for Windows', () {
      const platform = _FakePlatform(windows: true);
      expect(
        BaseUrlHelper.getBaseUrl(platform: platform),
        'http://127.0.0.1:8000',
      );
    });

    test('returns 127.0.0.1 for Linux', () {
      const platform = _FakePlatform(linux: true);
      expect(
        BaseUrlHelper.getBaseUrl(platform: platform),
        'http://127.0.0.1:8000',
      );
    });

    test('falls back to localhost when platform unknown', () {
      const platform = _FakePlatform();
      expect(
        BaseUrlHelper.getBaseUrl(platform: platform),
        'http://localhost:8000',
      );
    });
  });
}


