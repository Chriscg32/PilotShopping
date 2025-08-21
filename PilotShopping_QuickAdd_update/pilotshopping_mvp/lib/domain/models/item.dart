import 'package:hive/hive.dart';

part 'item.g.dart';

@HiveType(typeId: 0)
class Item {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String name;

  @HiveField(2)
  final List<String> barcodes;

  @HiveField(3)
  final String? notes;

  @HiveField(4)
  final double? lastPrice;

  @HiveField(5)
  final bool favoriteFlag;

  @HiveField(6)
  final DateTime updatedAt;

  Item({
    required this.id,
    required this.name,
    this.barcodes = const [],
    this.notes,
    this.lastPrice,
    this.favoriteFlag = false,
    required this.updatedAt,
  });

  Item copyWith({
    String? name,
    List<String>? barcodes,
    String? notes,
    double? lastPrice,
    bool? favoriteFlag,
    DateTime? updatedAt,
  }) {
    return Item(
      id: this.id,
      name: name ?? this.name,
      barcodes: barcodes ?? this.barcodes,
      notes: notes ?? this.notes,
      lastPrice: lastPrice ?? this.lastPrice,
      favoriteFlag: favoriteFlag ?? this.favoriteFlag,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'barcodes': barcodes,
      'notes': notes,
      'lastPrice': lastPrice,
      'favoriteFlag': favoriteFlag,
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'],
      name: json['name'],
      barcodes: List<String>.from(json['barcodes'] ?? []),
      notes: json['notes'],
      lastPrice: json['lastPrice'],
      favoriteFlag: json['favoriteFlag'] ?? false,
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }
}

class ItemAdapter extends TypeAdapter<Item> {
  @override
  final int typeId = 0;

  @override
  Item read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{};
    for (int i = 0; i < numOfFields; i++) {
      final key = reader.readByte();
      final value = reader.read();
      fields[key] = value;
    }
    return Item(
      id: fields[0] as String,
      name: fields[1] as String,
      barcodes: (fields[2] as List).cast<String>(),
      notes: fields[3] as String?,
      lastPrice: fields[4] as double?,
      favoriteFlag: fields[5] as bool,
      updatedAt: fields[6] as DateTime,
    );
  }

  @override
  void write(BinaryWriter writer, Item obj) {
    writer.writeByte(7);
    writer.writeByte(0);
    writer.write(obj.id);
    writer.writeByte(1);
    writer.write(obj.name);
    writer.writeByte(2);
    writer.write(obj.barcodes);
    writer.writeByte(3);
    writer.write(obj.notes);
    writer.writeByte(4);
    writer.write(obj.lastPrice);
    writer.writeByte(5);
    writer.write(obj.favoriteFlag);
    writer.writeByte(6);
    writer.write(obj.updatedAt);
  }
}
