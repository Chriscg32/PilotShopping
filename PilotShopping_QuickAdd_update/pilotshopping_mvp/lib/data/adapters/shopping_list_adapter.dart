import 'package:hive/hive.dart';
import '../../domain/models/shopping_list.dart';

class ShoppingListAdapter extends TypeAdapter<ShoppingList> {
  @override
  final int typeId = 1;

  @override
  ShoppingList read(BinaryReader reader) {
    final id = reader.readString();
    final name = reader.readString();
    final hasMonthKey = reader.readBool();
    final monthKey = hasMonthKey ? reader.readString() : null;
    final itemIdsLength = reader.readInt();
    final itemIds = <String>[];
    for (var i = 0; i < itemIdsLength; i++) {
      itemIds.add(reader.readString());
    }
    final createdAt = DateTime.parse(reader.readString());

    return ShoppingList(
      id: id,
      name: name,
      monthKey: monthKey,
      itemIds: itemIds,
      createdAt: createdAt,
    );
  }

  @override
  void write(BinaryWriter writer, ShoppingList obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.name);
    writer.writeBool(obj.monthKey != null);
    if (obj.monthKey != null) {
      writer.writeString(obj.monthKey!);
    }
    writer.writeInt(obj.itemIds.length);
    for (var itemId in obj.itemIds) {
      writer.writeString(itemId);
    }
    writer.writeString(obj.createdAt.toIso8601String());
  }
}
