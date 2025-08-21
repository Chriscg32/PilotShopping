import 'package:hive/hive.dart';
import '../../domain/models/settings.dart';

class SettingsAdapter extends TypeAdapter<Settings> {
  @override
  final int typeId = 4;

  @override
  Settings read(BinaryReader reader) {
    final hasSessionBudget = reader.readBool();
    final sessionBudget = hasSessionBudget ? reader.readDouble() : null;
    final hasWarnThreshold = reader.readBool();
    final warnThreshold = hasWarnThreshold ? reader.readDouble() : null;
    final hasCurrencyCode = reader.readBool();
    final currencyCode = hasCurrencyCode ? reader.readString() : 'USD';

    return Settings(
      sessionBudget: sessionBudget,
      warnThreshold: warnThreshold,
      currencyCode: currencyCode,
    );
  }

  @override
  void write(BinaryWriter writer, Settings obj) {
    writer.writeBool(obj.sessionBudget != null);
    if (obj.sessionBudget != null) {
      writer.writeDouble(obj.sessionBudget!);
    }
    writer.writeBool(obj.warnThreshold != null);
    if (obj.warnThreshold != null) {
      writer.writeDouble(obj.warnThreshold!);
    }
    writer.writeBool(obj.currencyCode != null);
    if (obj.currencyCode != null) {
      writer.writeString(obj.currencyCode!);
    }
  }
}
