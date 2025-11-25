import 'package:flutter/material.dart';

import 'utils/base_url_helper.dart';

void main() {
  runApp(const PQCMessengerApp());
}

class PQCMessengerApp extends StatelessWidget {
  const PQCMessengerApp({super.key});

  @override
  Widget build(BuildContext context) {
    final baseUrl = BaseUrlHelper.getBaseUrl();

    return MaterialApp(
      title: 'PQC Messenger',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('PQC Messenger'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Backend base URL:',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              Text(
                baseUrl,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ],
          ),
        ),
      ),
    );
  }
}


