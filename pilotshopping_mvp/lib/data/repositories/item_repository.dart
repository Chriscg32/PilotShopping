import 'package:pilotshopping_mvp/data/hive_boxes.dart';
import 'package:pilotshopping_mvp/domain/models/item.dart';

class ItemRepository {
  Box<Item> get _box => HiveBoxes.items;

  Future<void> saveItem(Item item) async {
    await _box.put(item.id, item);
  }

  Item? getItem(String id) {
    return _box.get(id);
  }

  List<Item> getAllItems() {
    return _box.values.toList();
  }

  Future<void> deleteItem(String id) async {
    await _box.delete(id);
  }

  Item? findByBarcode(String barcode) {
    return _box.values.firstWhere((item) => item.barcodes.contains(barcode));
  }
}