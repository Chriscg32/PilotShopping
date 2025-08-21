import 'package:hive/hive.dart';
import '../../domain/models/item.dart';

class ItemAdapter extends TypeAdapter<Item> {
  @override
  final int typeId = 0;

  @override
  Item read(BinaryReader reader) {
    final id = reader.readString();
    final name = reader.readString();
    final barcodesLength = reader.readInt();
    final barcodes = <String>[];
    for (var i = 0; i < barcodesLength; i++) {
      barcodes.add(reader.readString());
    }
    final hasNotes = reader.readBool();
    final notes = hasNotes ? reader.readString() : null;
    final hasLastPrice = reader.readBool();
    final lastPrice = hasLastPrice ? reader.readDouble() : null;
    final favoriteFlag = reader.readBool();
    final updatedAt = DateTime.parse(reader.readString());

    return Item(
      id: id,
      name: name,
      barcodes: barcodes,
      notes: notes,
      lastPrice: lastPrice,
      favoriteFlag: favoriteFlag,
      updatedAt: updatedAt,
    );
  }

  @override
  void write(BinaryWriter writer, Item obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.name);
    writer.writeInt(obj.barcodes.length);
    for (var barcode in obj.barcodes) {
      writer.writeString(barcode);
    }
    writer.writeBool(obj.notes != null);
    if (obj.notes != null) {
      writer.writeString(obj.notes!);
    }
    writer.writeBool(obj.lastPrice != null);
    if (obj.lastPrice != null) {
      writer.writeDouble(obj.lastPrice!);
    }
    writer.writeBool(obj.favoriteFlag);
    writer.writeString(obj.updatedAt.toIso8601String());
  }
}
