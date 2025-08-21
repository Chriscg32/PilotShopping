import 'package:hive/hive.dart';
import 'package:pilotshopping_mvp/domain/models/purchase_line.dart';

class PurchaseLineAdapter extends TypeAdapter<PurchaseLine> {
  @override
  final int typeId = 2;

  @override
  PurchaseLine read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return PurchaseLine(
      id: fields[0] as String,
      listId: fields[1] as String,
      itemId: fields[2] as String,
      qty: fields[3] as int,
      unitPrice: fields[4] as double,
      timestamp: fields[6] as DateTime,
    );
  }

  @override
  void write(BinaryWriter writer, PurchaseLine obj) {
    writer
      ..writeByte(7)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.listId)
      ..writeByte(2)
      ..write(obj.itemId)
      ..writeByte(3)
      ..write(obj.qty)
      ..writeByte(4)
      ..write(obj.unitPrice)
      ..writeByte(5)
      ..write(obj.total)
      ..writeByte(6)
      ..write(obj.timestamp);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is PurchaseLineAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}