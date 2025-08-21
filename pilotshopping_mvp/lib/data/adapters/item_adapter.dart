'''import 'package:hive/hive.dart';
import 'package:pilotshopping_mvp/domain/models/item.dart';

class ItemAdapter extends TypeAdapter<Item> {
  @override
  final int typeId = 0;

  @override
  Item read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return Item(
      id: fields[0] as String,
      name: fields[1] as String,
      barcodes: (fields[2] as List).cast<String>(),
      notes: fields[3] as String?,
      lastPrice: fields[4] as double?,
      favoriteFlag: fields[5] as bool?,
      updatedAt: fields[6] as DateTime,
    );
  }

  @override
  void write(BinaryWriter writer, Item obj) {
    writer
      ..writeByte(7)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.name)
      ..writeByte(2)
      ..write(obj.barcodes)
      ..writeByte(3)
      ..write(obj.notes)
      ..writeByte(4)
      ..write(obj.lastPrice)
      ..writeByte(5)
      ..write(obj.favoriteFlag)
      ..writeByte(6)
      ..write(obj.updatedAt);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ItemAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
''