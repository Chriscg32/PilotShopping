import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../data/repositories/item_repository.dart';
import '../../../data/repositories/shopping_list_repository.dart';
import '../../../services/barcode_scanner_service.dart';
import '../../widgets/common/custom_app_bar.dart';
import '../quick_add/quick_add_screen.dart';
import '../settings/settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;
  final List<String> _tabTitles = ['Shopping Lists', 'Items', 'Receipts'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: _tabTitles[_currentIndex],
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Search coming soon!')),
              );
            },
          ),
          if (_currentIndex == 1) // Only show barcode scanner on Items tab
            IconButton(
              icon: const Icon(Icons.qr_code_scanner),
              onPressed: _scanBarcode,
            ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: _buildBody(),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.list),
            label: 'Lists',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.shopping_cart),
            label: 'Items',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt),
            label: 'Receipts',
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _handleFabPressed,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody() {
    switch (_currentIndex) {
      case 0:
        return const Center(child: Text('Shopping Lists Tab'));
      case 1:
        return const Center(child: Text('Items Tab'));
      case 2:
        return const Center(child: Text('Receipts Tab'));
      default:
        return const SizedBox.shrink();
    }
  }

  void _handleFabPressed() {
    switch (_currentIndex) {
      case 0:
        // TODO: Navigate to create shopping list screen
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Create shopping list coming soon!')),
        );
        break;
      case 1:
        _navigateToQuickAdd();
        break;
      case 2:
        // TODO: Navigate to create receipt screen
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Create receipt coming soon!')),
        );
        break;
    }
  }

  Future<void> _scanBarcode() async {
    final barcodeScannerService = context.read<BarcodeScannerService>();
    final barcode = await barcodeScannerService.scanBarcode();
    
    if (barcode != null && mounted) {
      _navigateToQuickAdd(barcode: barcode);
    }
  }

  Future<void> _navigateToQuickAdd({String? barcode}) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => QuickAddScreen(barcode: barcode),
      ),
    );
    
    if (result == true && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Item added successfully!')),
      );
    }
  }
}
