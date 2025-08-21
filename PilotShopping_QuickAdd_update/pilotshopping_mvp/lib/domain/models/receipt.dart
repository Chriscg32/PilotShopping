import 'package:hive/hive.dart';

part 'receipt.g.dart';

@HiveType(typeId: 3)
class Receipt {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String storeName;

  @HiveField(2)
  final DateTime purchaseDate;

  @HiveField(3)
  final double totalAmount;

  @HiveField(4)
  final String? notes;

  Receipt({
    required this.id,
    required this.storeName,
    required this.purchaseDate,
    required this.totalAmount,
    this.notes,
  });

  Receipt copyWith({
    String? storeName,
    DateTime? purchaseDate,
    double? totalAmount,
    String? notes,
  }) {
    return Receipt(
      id: this.id,
      storeName: storeName ?? this.storeName,
      purchaseDate: purchaseDate ?? this.purchaseDate,
      totalAmount: totalAmount ?? this.totalAmount,
      notes: notes ?? this.notes,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'storeName': storeName,
      'purchaseDate': purchaseDate.toIso8601String(),
      'totalAmount': totalAmount,
      'notes': notes,
    };
  }

  factory Receipt.fromJson(Map<String, dynamic> json) {
    return Receipt(
      id: json['id'],
      storeName: json['storeName'],
      purchaseDate: DateTime.parse(json['purchaseDate']),
      totalAmount: json['totalAmount'],
      notes: json['notes'],
    );
  }
}

class ReceiptAdapter extends TypeAdapter<Receipt> {
  @override
  final int typeId = 3;

  @override
  Receipt read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{};
    for (int i = 0; i < numOfFields; i++) {
      final key = reader.readByte();
      final value = reader.read();
      fields[key] = value;
    }
    return Receipt(
      id: fields[0] as String,
      storeName: fields[1] as String,
      purchaseDate: fields[2] as DateTime,
      totalAmount: fields[3] as double,
      notes: fields[4] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, Receipt obj) {
    writer.writeByte(5);
    writer.writeByte(0);
    writer.write(obj.id);
    writer.writeByte(1);
    writer.write(obj.storeName);
    writer.writeByte(2);
    writer.write(obj.purchaseDate);
    writer.writeByte(3);
    writer.write(obj.totalAmount);
    writer.writeByte(4);
    writer.write(obj.notes);
  }
}
