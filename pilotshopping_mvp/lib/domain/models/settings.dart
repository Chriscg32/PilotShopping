import 'package:hive/hive.dart';

part 'settings.g.dart';

@HiveType(typeId: 4)
class Settings extends HiveObject {
  @HiveField(0)
  double? sessionBudget;

  @HiveField(1)
  double? warnThreshold;

  @HiveField(2)
  String? currencyCode;

  Settings({
    this.sessionBudget,
    this.warnThreshold,
    this.currencyCode,
  });
}