import 'package:hive/hive.dart';
import 'package:uuid/uuid.dart';

part 'purchase_line.g.dart';

@HiveType(typeId: 2)
class PurchaseLine extends HiveObject {
  @HiveField(0)
  String id;

  @HiveField(1)
  String listId;

  @HiveField(2)
  String itemId;

  @HiveField(3)
  int qty;

  @HiveField(4)
  double unitPrice;

  @HiveField(5)
  double get total => qty * unitPrice;

  @HiveField(6)
  DateTime timestamp;

  PurchaseLine({
    required this.id,
    required this.listId,
    required this.itemId,
    required this.qty,
    required this.unitPrice,
    required this.timestamp,
  });

  factory PurchaseLine.create({
    required String listId,
    required String itemId,
    required int qty,
    required double unitPrice,
  }) =>
      PurchaseLine(
        id: Uuid().v4(),
        listId: listId,
        itemId: itemId,
        qty: qty,
        unitPrice: unitPrice,
        timestamp: DateTime.now(),
      );
}