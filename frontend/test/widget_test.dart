import 'package:flutter_test/flutter_test.dart';

import 'package:pqc_messenger/main.dart';

void main() {
  testWidgets('app renders base URL helper text', (widgetTester) async {
    await widgetTester.pumpWidget(const PQCMessengerApp());

    expect(find.textContaining('Backend base URL'), findsOneWidget);
  });
}
