// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'receipt.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

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
      storeName: fields[1] as String,
      purchaseDate: fields[2] as DateTime,
      totalAmount: fields[3] as double,
      notes: fields[4] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, Receipt obj) {
    writer
      ..writeByte(5)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.storeName)
      ..writeByte(2)
      ..write(obj.purchaseDate)
      ..writeByte(3)
      ..write(obj.totalAmount)
      ..writeByte(4)
      ..write(obj.notes);
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
