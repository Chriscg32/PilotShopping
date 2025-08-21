import 'package:flutter/material.dart';

class ListDetailScreen extends StatelessWidget {
  const ListDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('List Details'),
      ),
      body: Center(
        child: Text('List Detail Screen'),
      ),
    );
  }
}