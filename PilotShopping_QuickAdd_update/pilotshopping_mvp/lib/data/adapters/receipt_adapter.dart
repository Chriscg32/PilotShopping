import 'package:hive/hive.dart';
import '../../domain/models/receipt.dart';

class ReceiptAdapter extends TypeAdapter<Receipt> {
  @override
  final int typeId = 3;

  @override
  Receipt read(BinaryReader reader) {
    final id = reader.readString();
    final listId = reader.readString();
    final imageBytesLength = reader.readInt();
    final imageBytes = <int>[];
    for (var i = 0; i < imageBytesLength; i++) {
      imageBytes.add(reader.readByte());
    }
    final hasReceiptBarcode = reader.readBool();
    final receiptBarcode = hasReceiptBarcode ? reader.readString() : null;
    final timestamp = DateTime.parse(reader.readString());

    return Receipt(
      id: id,
      listId: listId,
      imageBytes: imageBytes,
      receiptBarcode: receiptBarcode,
      timestamp: timestamp,
    );
  }

  @override
  void write(BinaryWriter writer, Receipt obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.listId);
    writer.writeInt(obj.imageBytes.length);
    for (var byte in obj.imageBytes) {
      writer.writeByte(byte);
    }
    writer.writeBool(obj.receiptBarcode != null);
    if (obj.receiptBarcode != null) {
      writer.writeString(obj.receiptBarcode!);
    }
    writer.writeString(obj.timestamp.toIso8601String());
  }
}
