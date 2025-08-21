import 'package:hive/hive.dart';
import '../../domain/models/purchase_line.dart';

class PurchaseLineRepository {
  final Box<PurchaseLine> _purchaseLineBox;

  PurchaseLineRepository(this._purchaseLineBox);

  List<PurchaseLine> getAllPurchaseLines() {
    return _purchaseLineBox.values.toList();
  }

  PurchaseLine? getPurchaseLineById(String id) {
    return _purchaseLineBox.get(id);
  }

  List<PurchaseLine> getPurchaseLinesByReceiptId(String receiptId) {
    return _purchaseLineBox.values
        .where((line) => line.receiptId == receiptId)
        .toList();
  }

  List<PurchaseLine> getPurchaseLinesByItemId(String itemId) {
    return _purchaseLineBox.values
        .where((line) => line.itemId == itemId)
        .toList();
  }

  Future<void> savePurchaseLine(PurchaseLine purchaseLine) async {
    await _purchaseLineBox.put(purchaseLine.id, purchaseLine);
  }

  Future<void> deletePurchaseLine(String id) async {
    await _purchaseLineBox.delete(id);
  }

  Future<void> deletePurchaseLinesByReceiptId(String receiptId) async {
    final linesToDelete = getPurchaseLinesByReceiptId(receiptId);
    for (final line in linesToDelete) {
      await _purchaseLineBox.delete(line.id);
    }
  }
}
