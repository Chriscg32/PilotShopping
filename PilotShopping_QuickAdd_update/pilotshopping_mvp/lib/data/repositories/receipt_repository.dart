import 'package:hive/hive.dart';
import '../../domain/models/receipt.dart';

class ReceiptRepository {
  final Box<Receipt> _receiptBox;

  ReceiptRepository(this._receiptBox);

  List<Receipt> getAllReceipts() {
    return _receiptBox.values.toList();
  }

  Receipt? getReceiptById(String id) {
    return _receiptBox.get(id);
  }

  List<Receipt> getReceiptsByDateRange(DateTime startDate, DateTime endDate) {
    return _receiptBox.values
        .where((receipt) =>
            receipt.purchaseDate.isAfter(startDate) &&
            receipt.purchaseDate.isBefore(endDate.add(const Duration(days: 1))))
        .toList();
  }

  Future<void> saveReceipt(Receipt receipt) async {
    await _receiptBox.put(receipt.id, receipt);
  }

  Future<void> deleteReceipt(String id) async {
    await _receiptBox.delete(id);
  }
}
