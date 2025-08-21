import 'package:hive/hive.dart';
import 'package:pilotshopping_mvp/domain/models/settings.dart';

class SettingsAdapter extends TypeAdapter<Settings> {
  @override
  final int typeId = 4;

  @override
  Settings read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return Settings(
      sessionBudget: fields[0] as double?,
      warnThreshold: fields[1] as double?,
      currencyCode: fields[2] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, Settings obj) {
    writer
      ..writeByte(3)
      ..writeByte(0)
      ..write(obj.sessionBudget)
      ..writeByte(1)
      ..write(obj.warnThreshold)
      ..writeByte(2)
      ..write(obj.currencyCode);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SettingsAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}