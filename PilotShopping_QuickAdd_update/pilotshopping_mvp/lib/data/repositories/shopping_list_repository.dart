import 'package:hive/hive.dart';
import '../../domain/models/shopping_list.dart';

class ShoppingListRepository {
  final Box<ShoppingList> _shoppingListBox;

  ShoppingListRepository(this._shoppingListBox);

  List<ShoppingList> getAllShoppingLists() {
    return _shoppingListBox.values.toList();
  }

  ShoppingList? getShoppingListById(String id) {
    return _shoppingListBox.get(id);
  }

  List<ShoppingList> getShoppingListsByMonthKey(String monthKey) {
    return _shoppingListBox.values
        .where((list) => list.monthKey == monthKey)
        .toList();
  }

  Future<void> saveShoppingList(ShoppingList shoppingList) async {
    await _shoppingListBox.put(shoppingList.id, shoppingList);
  }

  Future<void> deleteShoppingList(String id) async {
    await _shoppingListBox.delete(id);
  }

  Future<void> addItemToShoppingList(String listId, String itemId) async {
    final shoppingList = _shoppingListBox.get(listId);
    if (shoppingList != null) {
      if (!shoppingList.itemIds.contains(itemId)) {
        final updatedItemIds = List<String>.from(shoppingList.itemIds)..add(itemId);
        final updatedList = shoppingList.copyWith(itemIds: updatedItemIds);
        await _shoppingListBox.put(listId, updatedList);
      }
    }
  }

  Future<void> removeItemFromShoppingList(String listId, String itemId) async {
    final shoppingList = _shoppingListBox.get(listId);
    if (shoppingList != null) {
      final updatedItemIds = List<String>.from(shoppingList.itemIds)..remove(itemId);
      final updatedList = shoppingList.copyWith(itemIds: updatedItemIds);
      await _shoppingListBox.put(listId, updatedList);
    }
  }
}
