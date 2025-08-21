import 'package:hive/hive.dart';
import 'package:uuid/uuid.dart';

part 'receipt.g.dart';

@HiveType(typeId: 3)
class Receipt extends HiveObject {
  @HiveField(0)
  String id;

  @HiveField(1)
  String listId;

  @HiveField(2)
  List<int> imageBytes;

  @HiveField(3)
  String? receiptBarcode;

  @HiveField(4)
  DateTime timestamp;

  Receipt({
    required this.id,
    required this.listId,
    required this.imageBytes,
    this.receiptBarcode,
    required this.timestamp,
  });

  factory Receipt.create({
    required String listId,
    required List<int> imageBytes,
    String? receiptBarcode,
  }) =>
      Receipt(
        id: Uuid().v4(),
        listId: listId,
        imageBytes: imageBytes,
        receiptBarcode: receiptBarcode,
        timestamp: DateTime.now(),
      );
}