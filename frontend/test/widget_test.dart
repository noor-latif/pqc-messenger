import 'package:flutter_test/flutter_test.dart';

import 'package:pqc_messenger/main.dart';

void main() {
  testWidgets('onboarding screen renders hero copy', (widgetTester) async {
    await widgetTester.pumpWidget(const PQCMessengerRoot());
    await widgetTester.pumpAndSettle();

    expect(find.text('Post-Quantum Secure Messaging'), findsOneWidget);
    expect(find.text('Get Started'), findsOneWidget);
  });
}
