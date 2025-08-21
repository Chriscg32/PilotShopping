import 'package:hive/hive.dart';
import 'package:pilotshopping_mvp/domain/models/receipt.dart';

class ReceiptAdapter extends TypeAdapter<Receipt> {
  @override
  final int typeId = 3;

  @override
  Receipt read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return Receipt(
      id: fields[0] as String,
      listId: fields[1] as String,
      imageBytes: (fields[2] as List).cast<int>(),
      receiptBarcode: fields[3] as String?,
      timestamp: fields[4] as DateTime,
    );
  }

  @override
  void write(BinaryWriter writer, Receipt obj) {
    writer
      ..writeByte(5)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.listId)
      ..writeByte(2)
      ..write(obj.imageBytes)
      ..writeByte(3)
      ..write(obj.receiptBarcode)
      ..writeByte(4)
      ..write(obj.timestamp);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ReceiptAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}