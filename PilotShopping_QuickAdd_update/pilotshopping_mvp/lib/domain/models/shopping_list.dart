import 'package:hive/hive.dart';

part 'shopping_list.g.dart';

@HiveType(typeId: 1)
class ShoppingList {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String name;

  @HiveField(2)
  final String monthKey; // Format: YYYY-MM

  @HiveField(3)
  final List<String> itemIds;

  @HiveField(4)
  final DateTime createdAt;

  ShoppingList({
    required this.id,
    required this.name,
    required this.monthKey,
    this.itemIds = const [],
    required this.createdAt,
  });

  ShoppingList copyWith({
    String? name,
    String? monthKey,
    List<String>? itemIds,
    DateTime? createdAt,
  }) {
    return ShoppingList(
      id: this.id,
      name: name ?? this.name,
      monthKey: monthKey ?? this.monthKey,
      itemIds: itemIds ?? this.itemIds,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'monthKey': monthKey,
      'itemIds': itemIds,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  factory ShoppingList.fromJson(Map<String, dynamic> json) {
    return ShoppingList(
      id: json['id'],
      name: json['name'],
      monthKey: json['monthKey'],
      itemIds: List<String>.from(json['itemIds'] ?? []),
      createdAt: DateTime.parse(json['createdAt']),
    );
  }
}

class ShoppingListAdapter extends TypeAdapter<ShoppingList> {
  @override
  final int typeId = 1;

  @override
  ShoppingList read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{};
    for (int i = 0; i < numOfFields; i++) {
      final key = reader.readByte();
      final value = reader.read();
      fields[key] = value;
    }
    return ShoppingList(
      id: fields[0] as String,
      name: fields[1] as String,
      monthKey: fields[2] as String,
      itemIds: (fields[3] as List).cast<String>(),
      createdAt: fields[4] as DateTime,
    );
  }

  @override
  void write(BinaryWriter writer, ShoppingList obj) {
    writer.writeByte(5);
    writer.writeByte(0);
    writer.write(obj.id);
    writer.writeByte(1);
    writer.write(obj.name);
    writer.writeByte(2);
    writer.write(obj.monthKey);
    writer.writeByte(3);
    writer.write(obj.itemIds);
    writer.writeByte(4);
    writer.write(obj.createdAt);
  }
}
