import 'package:hive/hive.dart';
import '../../domain/models/purchase_line.dart';

class PurchaseLineAdapter extends TypeAdapter<PurchaseLine> {
  @override
  final int typeId = 2;

  @override
  PurchaseLine read(BinaryReader reader) {
    final id = reader.readString();
    final listId = reader.readString();
    final itemId = reader.readString();
    final qty = reader.readDouble();
    final unitPrice = reader.readDouble();
    final total = reader.readDouble();
    final timestamp = DateTime.parse(reader.readString());

    return PurchaseLine(
      id: id,
      listId: listId,
      itemId: itemId,
      qty: qty,
      unitPrice: unitPrice,
      total: total,
      timestamp: timestamp,
    );
  }

  @override
  void write(BinaryWriter writer, PurchaseLine obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.listId);
    writer.writeString(obj.itemId);
    writer.writeDouble(obj.qty);
    writer.writeDouble(obj.unitPrice);
    writer.writeDouble(obj.total);
    writer.writeString(obj.timestamp.toIso8601String());
  }
}
