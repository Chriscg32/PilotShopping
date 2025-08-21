import 'package:hive/hive.dart';
import 'package:uuid/uuid.dart';

part 'shopping_list.g.dart';

@HiveType(typeId: 1)
class ShoppingList extends HiveObject {
  @HiveField(0)
  String id;

  @HiveField(1)
  String name;

  @HiveField(2)
  String? monthKey;

  @HiveField(3)
  List<String> itemIds;

  ShoppingList({
    required this.id,
    required this.name,
    this.monthKey,
    required this.itemIds,
  });

  factory ShoppingList.create({
    required String name,
    String? monthKey,
    List<String>? itemIds,
  }) =>
      ShoppingList(
        id: Uuid().v4(),
        name: name,
        monthKey: monthKey,
        itemIds: itemIds ?? [],
      );
}