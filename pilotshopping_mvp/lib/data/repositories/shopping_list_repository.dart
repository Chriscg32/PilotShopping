import 'package:pilotshopping_mvp/data/hive_boxes.dart';
import 'package:pilotshopping_mvp/domain/models/shopping_list.dart';

class ShoppingListRepository {
  Box<ShoppingList> get _box => HiveBoxes.shoppingLists;

  Future<void> saveShoppingList(ShoppingList list) async {
    await _box.put(list.id, list);
  }

  ShoppingList? getShoppingList(String id) {
    return _box.get(id);
  }

  List<ShoppingList> getAllShoppingLists() {
    return _box.values.toList();
  }

  Future<void> deleteShoppingList(String id) async {
    await _box.delete(id);
  }
}