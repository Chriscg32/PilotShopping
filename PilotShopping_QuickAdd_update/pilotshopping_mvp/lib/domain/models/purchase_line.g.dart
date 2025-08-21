// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'purchase_line.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

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
      receiptId: fields[1] as String,
      itemId: fields[2] as String,
      quantity: fields[3] as double,
      price: fields[4] as double,
      notes: fields[5] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, PurchaseLine obj) {
    writer
      ..writeByte(6)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.receiptId)
      ..writeByte(2)
      ..write(obj.itemId)
      ..writeByte(3)
      ..write(obj.quantity)
      ..writeByte(4)
      ..write(obj.price)
      ..writeByte(5)
      ..write(obj.notes);
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
