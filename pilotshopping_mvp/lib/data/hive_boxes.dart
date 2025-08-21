import 'package:hive_flutter/hive_flutter.dart';

class HiveBoxes {
  static const String items = 'items';
  static const String shoppingLists = 'shoppingLists';
  static const String purchaseLines = 'purchaseLines';
  static const String receipts = 'receipts';
  static const String settings = 'settings';

  static Future<void> init() async {
    await Hive.initFlutter();
    
    // Register adapters
    Hive.registerAdapter(ItemAdapter());
    Hive.registerAdapter(ShoppingListAdapter());
    Hive.registerAdapter(PurchaseLineAdapter());
    Hive.registerAdapter(ReceiptAdapter());
    Hive.registerAdapter(SettingsAdapter());
    
    // Open boxes
    await Hive.openBox<Item>(items);
    await Hive.openBox<ShoppingList>(shoppingLists);
    await Hive.openBox<PurchaseLine>(purchaseLines);
    await Hive.openBox<Receipt>(receipts);
    await Hive.openBox<Settings>(settings);
  }
}

// Placeholder adapters - will be implemented in adapters/
class ItemAdapter extends TypeAdapter<Item> {
  @override
  final int typeId = 0;
  
  @override
  Item read(BinaryReader reader) {
    return Item(
      id: reader.readString(),
      name: reader.readString(),
      barcodes: List<String>.from(reader.readList()),
      notes: reader.readString(),
      lastPrice: reader.readDouble(),
      favoriteFlag: reader.readBool(),
      updatedAt: DateTime.fromMillisecondsSinceEpoch(reader.readInt()),
    );
  }

  @override
  void write(BinaryWriter writer, Item obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.name);
    writer.writeList(obj.barcodes);
    writer.writeString(obj.notes ?? '');
    writer.writeDouble(obj.lastPrice ?? 0.0);
    writer.writeBool(obj.favoriteFlag ?? false);
    writer.writeInt(obj.updatedAt.millisecondsSinceEpoch);
  }
}

class ShoppingListAdapter extends TypeAdapter<ShoppingList> {
  @override
  final int typeId = 1;
  
  @override
  ShoppingList read(BinaryReader reader) {
    return ShoppingList(
      id: reader.readString(),
      name: reader.readString(),
      monthKey: reader.readString(),
      itemIds: List<String>.from(reader.readList()),
    );
  }

  @override
  void write(BinaryWriter writer, ShoppingList obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.name);
    writer.writeString(obj.monthKey ?? '');
    writer.writeList(obj.itemIds);
  }
}

class PurchaseLineAdapter extends TypeAdapter<PurchaseLine> {
  @override
  final int typeId = 2;
  
  @override
  PurchaseLine read(BinaryReader reader) {
    return PurchaseLine(
      id: reader.readString(),
      listId: reader.readString(),
      itemId: reader.readString(),
      qty: reader.readDouble(),
      unitPrice: reader.readDouble(),
      total: reader.readDouble(),
      timestamp: DateTime.fromMillisecondsSinceEpoch(reader.readInt()),
    );
  }

  @override
  void write(BinaryWriter writer, PurchaseLine obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.listId);
    writer.writeString(obj.itemId);
    writer.writeDouble(obj.qty);
    writer.writeDouble(obj.unitPrice);
    writer.writeDouble(obj.total);
    writer.writeInt(obj.timestamp.millisecondsSinceEpoch);
  }
}

class ReceiptAdapter extends TypeAdapter<Receipt> {
  @override
  final int typeId = 3;
  
  @override
  Receipt read(BinaryReader reader) {
    return Receipt(
      id: reader.readString(),
      listId: reader.readString(),
      imageBytes: reader.readList() as List<int>,
      receiptBarcode: reader.readString(),
      timestamp: DateTime.fromMillisecondsSinceEpoch(reader.readInt()),
    );
  }

  @override
  void write(BinaryWriter writer, Receipt obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.listId);
    writer.writeList(obj.imageBytes);
    writer.writeString(obj.receiptBarcode ?? '');
    writer.writeInt(obj.timestamp.millisecondsSinceEpoch);
  }
}

class SettingsAdapter extends TypeAdapter<Settings> {
  @override
  final int typeId = 4;
  
  @override
  Settings read(BinaryReader reader) {
    return Settings(
      sessionBudget: reader.readDouble(),
      warnThreshold: reader.readDouble(),
      currencyCode: reader.readString(),
    );
  }

  @override
  void write(BinaryWriter writer, Settings obj) {
    writer.writeDouble(obj.sessionBudget ?? 0.0);
    writer.writeDouble(obj.warnThreshold ?? 0.0);
    writer.writeString(obj.currencyCode ?? 'USD');
  }
}

// Model classes
class Item {
  final String id;
  final String name;
  final List<String> barcodes;
  final String? notes;
  final double? lastPrice;
  final bool? favoriteFlag;
  final DateTime updatedAt;

  Item({
    required this.id,
    required this.name,
    this.barcodes = const [],
    this.notes,
    this.lastPrice,
    this.favoriteFlag,
    required this.updatedAt,
  });
}

class ShoppingList {
  final String id;
  final String name;
  final String? monthKey;
  final List<String> itemIds;

  ShoppingList({
    required this.id,
    required this.name,
    this.monthKey,
    this.itemIds = const [],
  });
}

class PurchaseLine {
  final String id;
  final String listId;
  final String itemId;
  final double qty;
  final double unitPrice;
  final double total;
  final DateTime timestamp;

  PurchaseLine({
    required this.id,
    required this.listId,
    required this.itemId,
    required this.qty,
    required this.unitPrice,
    required this.total,
    required this.timestamp,
  });
}

class Receipt {
  final String id;
  final String listId;
  final List<int> imageBytes;
  final String? receiptBarcode;
  final DateTime timestamp;

  Receipt({
    required this.id,
    required this.listId,
    required this.imageBytes,
    this.receiptBarcode,
    required this.timestamp,
  });
}

class Settings {
  final double? sessionBudget;
  final double? warnThreshold;
  final String? currencyCode;

  Settings({
    this.sessionBudget,
    this.warnThreshold,
    this.currencyCode,
  });
}
