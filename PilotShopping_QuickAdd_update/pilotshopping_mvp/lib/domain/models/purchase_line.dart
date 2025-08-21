import 'package:hive/hive.dart';

part 'purchase_line.g.dart';

@HiveType(typeId: 2)
class PurchaseLine {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String receiptId;

  @HiveField(2)
  final String itemId;

  @HiveField(3)
  final double quantity;

  @HiveField(4)
  final double price;

  @HiveField(5)
  final String? notes;

  PurchaseLine({
    required this.id,
    required this.receiptId,
    required this.itemId,
    required this.quantity,
    required this.price,
    this.notes,
  });

  PurchaseLine copyWith({
    String? receiptId,
    String? itemId,
    double? quantity,
    double? price,
    String? notes,
  }) {
    return PurchaseLine(
      id: this.id,
      receiptId: receiptId ?? this.receiptId,
      itemId: itemId ?? this.itemId,
      quantity: quantity ?? this.quantity,
      price: price ?? this.price,
      notes: notes ?? this.notes,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'receiptId': receiptId,
      'itemId': itemId,
      'quantity': quantity,
      'price': price,
      'notes': notes,
    };
  }

  factory PurchaseLine.fromJson(Map<String, dynamic> json) {
    return PurchaseLine(
      id: json['id'],
      receiptId: json['receiptId'],
      itemId: json['itemId'],
      quantity: json['quantity'],
      price: json['price'],
      notes: json['notes'],
    );
  }
}

class PurchaseLineAdapter extends TypeAdapter<PurchaseLine> {
  @override
  final int typeId = 2;

  @override
  PurchaseLine read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{};
    for (int i = 0; i < numOfFields; i++) {
      final key = reader.readByte();
      final value = reader.read();
      fields[key] = value;
    }
    return PurchaseLine(
      id: fields[0] as String,
      receiptId: fields[1] as String,
      itemId: fields[2] as String,
      quantity: fields[3] as double,
      price: fields[4] as double,
      notes: fields[5] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, PurchaseLine obj) {
    writer.writeByte(6);
    writer.writeByte(0);
    writer.write(obj.id);
    writer.writeByte(1);
    writer.write(obj.receiptId);
    writer.writeByte(2);
    writer.write(obj.itemId);
    writer.writeByte(3);
    writer.write(obj.quantity);
    writer.writeByte(4);
    writer.write(obj.price);
    writer.writeByte(5);
    writer.write(obj.notes);
  }
}
