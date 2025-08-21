import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';

import 'data/repositories/item_repository.dart';
import 'data/repositories/purchase_line_repository.dart';
import 'data/repositories/receipt_repository.dart';
import 'data/repositories/settings_repository.dart';
import 'data/repositories/shopping_list_repository.dart';
import 'domain/models/item.dart';
import 'domain/models/purchase_line.dart';
import 'domain/models/receipt.dart';
import 'domain/models/settings.dart';
import 'domain/models/shopping_list.dart';
import 'services/barcode_scanner_service.dart';
import 'services/quick_add_service.dart';
import 'ui/screens/home/home_screen.dart';
import 'ui/theme/app_theme.dart';
import 'ui/theme/theme_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Hive
  await Hive.initFlutter();

  // Register adapters
  Hive.registerAdapter(ItemAdapter());
  Hive.registerAdapter(ShoppingListAdapter());
  Hive.registerAdapter(PurchaseLineAdapter());
  Hive.registerAdapter(ReceiptAdapter());
  Hive.registerAdapter(SettingsAdapter());

  // Open boxes
  await Hive.openBox<Item>('items');
  await Hive.openBox<ShoppingList>('shoppingLists');
  await Hive.openBox<PurchaseLine>('purchaseLines');
  await Hive.openBox<Receipt>('receipts');
  await Hive.openBox<Settings>('settings');

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // Repositories
        Provider<ItemRepository>(
          create: (_) => ItemRepository(),
        ),
        Provider<ShoppingListRepository>(
          create: (_) => ShoppingListRepository(),
        ),
        Provider<PurchaseLineRepository>(
          create: (_) => PurchaseLineRepository(),
        ),
        Provider<ReceiptRepository>(
          create: (_) => ReceiptRepository(),
        ),
        Provider<SettingsRepository>(
          create: (_) => SettingsRepository(),
        ),
        
        // Services
        Provider<BarcodeScannerService>(
          create: (_) => BarcodeScannerService(),
        ),
        Provider<QuickAddService>(
          create: (context) => QuickAddService(
            itemRepository: context.read<ItemRepository>(),
            shoppingListRepository: context.read<ShoppingListRepository>(),
            barcodeScannerService: context.read<BarcodeScannerService>(),
          ),
        ),
        
        // Theme provider
        ChangeNotifierProvider<ThemeProvider>(
          create: (_) => ThemeProvider(),
        ),
      ],
      child: Consumer<ThemeProvider>(
        builder: (context, themeProvider, _) {
          return MaterialApp(
            title: 'PilotShopping',
            theme: AppTheme.lightTheme,
            darkTheme: AppTheme.darkTheme,
            themeMode: themeProvider.themeMode,
            home: const HomeScreen(),
            debugShowCheckedModeBanner: false,
          );
        },
      ),
    );
  }
}
