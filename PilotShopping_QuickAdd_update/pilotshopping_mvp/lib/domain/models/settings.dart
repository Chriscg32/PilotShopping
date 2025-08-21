import 'package:hive/hive.dart';

part 'settings.g.dart';

@HiveType(typeId: 4)
class Settings {
  @HiveField(0)
  final bool darkMode;

  @HiveField(1)
  final String defaultCurrency;

  @HiveField(2)
  final bool showPriceHistory;

  Settings({
    this.darkMode = false,
    this.defaultCurrency = 'USD',
    this.showPriceHistory = true,
  });

  Settings copyWith({
    bool? darkMode,
    String? defaultCurrency,
    bool? showPriceHistory,
  }) {
    return Settings(
      darkMode: darkMode ?? this.darkMode,
      defaultCurrency: defaultCurrency ?? this.defaultCurrency,
      showPriceHistory: showPriceHistory ?? this.showPriceHistory,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'darkMode': darkMode,
      'defaultCurrency': defaultCurrency,
      'showPriceHistory': showPriceHistory,
    };
  }

  factory Settings.fromJson(Map<String, dynamic> json) {
    return Settings(
      darkMode: json['darkMode'] ?? false,
      defaultCurrency: json['defaultCurrency'] ?? 'USD',
      showPriceHistory: json['showPriceHistory'] ?? true,
    );
  }
}

class SettingsAdapter extends TypeAdapter<Settings> {
  @override
  final int typeId = 4;

  @override
  Settings read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{};
    for (int i = 0; i < numOfFields; i++) {
      final key = reader.readByte();
      final value = reader.read();
      fields[key] = value;
    }
    return Settings(
      darkMode: fields[0] as bool,
      defaultCurrency: fields[1] as String,
      showPriceHistory: fields[2] as bool,
    );
  }

  @override
  void write(BinaryWriter writer, Settings obj) {
    writer.writeByte(3);
    writer.writeByte(0);
    writer.write(obj.darkMode);
    writer.writeByte(1);
    writer.write(obj.defaultCurrency);
    writer.writeByte(2);
    writer.write(obj.showPriceHistory);
  }
}
