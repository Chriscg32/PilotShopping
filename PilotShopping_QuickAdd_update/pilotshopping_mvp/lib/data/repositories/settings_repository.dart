import 'package:hive/hive.dart';
import '../../domain/models/settings.dart';

class SettingsRepository {
  final Box<Settings> _settingsBox;
  static const String _settingsKey = 'app_settings';

  SettingsRepository(this._settingsBox);

  Settings getSettings() {
    return _settingsBox.get(_settingsKey) ?? Settings();
  }

  Future<void> saveSettings(Settings settings) async {
    await _settingsBox.put(_settingsKey, settings);
  }

  Future<void> resetSettings() async {
    await _settingsBox.put(_settingsKey, Settings());
  }
}
