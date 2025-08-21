import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'data/hive_boxes.dart';
import 'ui/screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await HiveBoxes.init();
  runApp(const PilotShoppingApp());
}

class PilotShoppingApp extends StatelessWidget {
  const PilotShoppingApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PilotShopping',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
