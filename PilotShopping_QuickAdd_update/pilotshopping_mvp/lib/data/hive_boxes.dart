import 'package:hive_flutter/hive_flutter.dart';
import '../domain/models/models.dart';
import 'adapters/adapters.dart';

class HiveBoxes {
  static const String itemsBox = 'items';
  static const String shoppingListsBox = 'shoppingLists';
  static const String purchaseLinesBox = 'purchaseLines';
  static const String receiptsBox = 'receipts';
  static const String settingsBox = 'settings';

  static Future<void> init() async {
    await Hive.initFlutter();
    
    // Register adapters
    Hive.registerAdapter(ItemAdapter());
    Hive.registerAdapter(ShoppingListAdapter());
    Hive.registerAdapter(PurchaseLineAdapter());
    Hive.registerAdapter(ReceiptAdapter());
    Hive.registerAdapter(SettingsAdapter());
    
    // Open boxes
    await Hive.openBox<Item>(itemsBox);
    await Hive.openBox<ShoppingList>(shoppingListsBox);
    await Hive.openBox<PurchaseLine>(purchaseLinesBox);
    await Hive.openBox<Receipt>(receiptsBox);
    await Hive.openBox<Settings>(settingsBox);
  }

  // Box getters
  static Box<Item> get items => Hive.box<Item>(itemsBox);
  static Box<ShoppingList> get shoppingLists => Hive.box<ShoppingList>(shoppingListsBox);
  static Box<PurchaseLine> get purchaseLines => Hive.box<PurchaseLine>(purchaseLinesBox);
  static Box<Receipt> get receipts => Hive.box<Receipt>(receiptsBox);
  static Box<Settings> get settings => Hive.box<Settings>(settingsBox);

  // Settings singleton getter
  static Settings getSettings() {
    if (settings.isEmpty) {
      final defaultSettings = Settings();
      settings.put('settings', defaultSettings);
      return defaultSettings;
    }
    return settings.get('settings')!;
  }

  // Update settings
  static Future<void> updateSettings(Settings newSettings) async {
    await settings.put('settings', newSettings);
  }
}
