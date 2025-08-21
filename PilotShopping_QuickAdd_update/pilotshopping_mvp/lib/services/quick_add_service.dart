import '../data/repositories/item_repository.dart';
import '../data/repositories/shopping_list_repository.dart';
import '../domain/models/item.dart';
import 'barcode_scanner_service.dart';

class QuickAddService {
  final ItemRepository _itemRepository;
  final ShoppingListRepository _shoppingListRepository;
  final BarcodeScannerService _barcodeScannerService;

  QuickAddService(
    this._itemRepository,
    this._shoppingListRepository,
    this._barcodeScannerService,
  );

  Future<String?> scanBarcode() async {
    return await _barcodeScannerService.scanBarcode();
  }

  Future<Item?> getItemByBarcode(String barcode) async {
    final items = _itemRepository.getItemsByBarcode(barcode);
    return items.isNotEmpty ? items.first : null;
  }

  Future<void> quickAddItemToList({
    required String itemId,
    required String shoppingListId,
  }) async {
    await _shoppingListRepository.addItemToShoppingList(
      shoppingListId,
      itemId,
    );
  }

  Future<String> createOrUpdateItem({
    String? id,
    required String name,
    required List<String> barcodes,
    String? notes,
    double? lastPrice,
    bool favoriteFlag = false,
  }) async {
    final now = DateTime.now();
    
    // If id is provided, update existing item
    if (id != null && id.isNotEmpty) {
      final existingItem = _itemRepository.getItemById(id);
      if (existingItem != null) {
        final updatedItem = existingItem.copyWith(
          name: name,
          barcodes: barcodes,
          notes: notes,
          lastPrice: lastPrice ?? existingItem.lastPrice,
          favoriteFlag: favoriteFlag,
          updatedAt: now,
        );
        await _itemRepository.saveItem(updatedItem);
        return id;
      }
    }
    
    // Create new item
    final newItem = Item(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: name,
      barcodes: barcodes,
      notes: notes,
      lastPrice: lastPrice,
      favoriteFlag: favoriteFlag,
      updatedAt: now,
    );
    
    await _itemRepository.saveItem(newItem);
    return newItem.id;
  }
}
