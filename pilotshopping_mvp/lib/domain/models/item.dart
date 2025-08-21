import 'package:hive/hive.dart';
import 'package:uuid/uuid.dart';

part 'item.g.dart';

@HiveType(typeId: 0)
class Item extends HiveObject {
  @HiveField(0)
  String id;

  @HiveField(1)
  String name;

  @HiveField(2)
  List<String> barcodes;

  @HiveField(3)
  String? notes;

  @HiveField(4)
  double? lastPrice;

  @HiveField(5)
  bool? favoriteFlag;

  @HiveField(6)
  DateTime updatedAt;

  Item({
    required this.id,
    required this.name,
    required this.barcodes,
    this.notes,
    this.lastPrice,
    this.favoriteFlag,
    required this.updatedAt,
  });

  factory Item.create({
    required String name,
    List<String>? barcodes,
    String? notes,
  }) =>
      Item(
        id: Uuid().v4(),
        name: name,
        barcodes: barcodes ?? [],
        notes: notes,
        updatedAt: DateTime.now(),
      );
}