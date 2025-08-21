import 'package:hive/hive.dart';
import '../../domain/models/item.dart';

class ItemRepository {
  final Box<Item> _itemBox;

  ItemRepository(this._itemBox);

  List<Item> getAllItems() {
    return _itemBox.values.toList();
  }

  Item? getItemById(String id) {
    return _itemBox.get(id);
  }

  List<Item> getItemsByBarcode(String barcode) {
    return _itemBox.values
        .where((item) => item.barcodes.contains(barcode))
        .toList();
  }

  Future<void> saveItem(Item item) async {
    await _itemBox.put(item.id, item);
  }

  Future<void> deleteItem(String id) async {
    await _itemBox.delete(id);
  }

  List<Item> getFavoriteItems() {
    return _itemBox.values
        .where((item) => item.favoriteFlag)
        .toList();
  }

  Future<void> updateFavoriteFlag(String id, bool isFavorite) async {
    final item = _itemBox.get(id);
    if (item != null) {
      final updatedItem = item.copyWith(favoriteFlag: isFavorite);
      await _itemBox.put(id, updatedItem);
    }
  }

  Future<void> updateLastPrice(String id, double price) async {
    final item = _itemBox.get(id);
    if (item != null) {
      final updatedItem = item.copyWith(lastPrice: price);
      await _itemBox.put(id, updatedItem);
    }
  }
}
