import 'dart:io';
import 'package:csv/csv.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:file_picker/file_picker.dart';
import '../domain/models/models.dart';
import '../data/repositories/repositories.dart';

class ExportService {
  final ItemRepository _itemRepository;
  final ShoppingListRepository _shoppingListRepository;
  final PurchaseLineRepository _purchaseLineRepository;
  final ReceiptRepository _receiptRepository;

  ExportService({
    required ItemRepository itemRepository,
    required ShoppingListRepository shoppingListRepository,
    required PurchaseLineRepository purchaseLineRepository,
    required ReceiptRepository receiptRepository,
  })
      : _itemRepository = itemRepository,
        _shoppingListRepository = shoppingListRepository,
        _purchaseLineRepository = purchaseLineRepository,
        _receiptRepository = receiptRepository;

  // Export items to CSV
  Future<bool> exportItemsToCsv() async {
    try {
      final items = _itemRepository.getAllItems();
      final csvData = [
        // Header
        ['ID', 'Name', 'Description', 'Barcodes', 'Last Price', 'Favorite'],
        // Data rows
        ...items.map((item) => [
              item.id,
              item.name,
              item.description,
              item.barcodes.join(";"),
              item.lastPrice,
              item.favoriteFlag ? "Yes" : "No",
            ]),
      ];

      final csv = const ListToCsvConverter().convert(csvData);
      final directory = await FilePicker.platform.getDirectoryPath();
      if (directory == null) return false;

      final file = File("$directory/items_export.csv");
      await file.writeAsString(csv);
      return true;
    } catch (e) {
      print("Error exporting items to CSV: $e");
      return false;
    }
  }

  // Export shopping list to PDF
  Future<bool> exportShoppingListToPdf(String listId) async {
    try {
      final shoppingList = _shoppingListRepository.getShoppingListById(listId);
      if (shoppingList == null) return false;

      final purchaseLines = _purchaseLineRepository.getPurchaseLinesByListId(listId);
      final items = _itemRepository.getAllItems();

      // Create PDF document
      final pdf = pw.Document();

      // Add page
      pdf.addPage(
        pw.Page(
          build: (pw.Context context) {
            return pw.Column(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Header(level: 0, text: "Shopping List: ${shoppingList.name}"),
                pw.SizedBox(height: 20),
                pw.Text("Date: ${shoppingList.createdAt.toString().substring(0, 10)}"),
                pw.SizedBox(height: 10),
                pw.Text("Month: ${shoppingList.monthKey}"),
                pw.SizedBox(height: 20),
                pw.Table(
                  border: pw.TableBorder.all(),
                  columnWidths: {
                    0: const pw.FlexColumnWidth(1),
                    1: const pw.FlexColumnWidth(3),
                    2: const pw.FlexColumnWidth(1),
                    3: const pw.FlexColumnWidth(1),
                    4: const pw.FlexColumnWidth(1),
                  },
                  children: [
                    // Header row
                    pw.TableRow(
                      children: [
                        pw.Padding(
                          padding: const pw.EdgeInsets.all(5),
                          child: pw.Text("#", style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                        ),
                        pw.Padding(
                          padding: const pw.EdgeInsets.all(5),
                          child: pw.Text("Item", style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                        ),
                        pw.Padding(
                          padding: const pw.EdgeInsets.all(5),
                          child: pw.Text("Quantity", style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                        ),
                        pw.Padding(
                          padding: const pw.EdgeInsets.all(5),
                          child: pw.Text("Price", style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                        ),
                        pw.Padding(
                          padding: const pw.EdgeInsets.all(5),
                          child: pw.Text("Total", style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                        ),
                      ],
                    ),
                    // Data rows
                    ...purchaseLines.asMap().entries.map((entry) {
                      final index = entry.key;
                      final line = entry.value;
                      final item = items.firstWhere(
                        (i) => i.id == line.itemId,
                        orElse: () => Item(
                          id: "unknown",
                          name: "Unknown Item",
                          description: "",
                          barcodes: [],
                          lastPrice: 0,
                          favoriteFlag: false,
                        ),
                      );

                      return pw.TableRow(
                        children: [
                          pw.Padding(
                            padding: const pw.EdgeInsets.all(5),
                            child: pw.Text("${index + 1}"),
                          ),
                          pw.Padding(
                            padding: const pw.EdgeInsets.all(5),
                            child: pw.Text(item.name),
                          ),
                          pw.Padding(
                            padding: const pw.EdgeInsets.all(5),
                            child: pw.Text(line.quantity.toString()),
                          ),
                          pw.Padding(
                            padding: const pw.EdgeInsets.all(5),
                            child: pw.Text(line.price.toStringAsFixed(2)),
                          ),
                          pw.Padding(
                            padding: const pw.EdgeInsets.all(5),
                            child: pw.Text(line.total.toStringAsFixed(2)),
                          ),
                        ],
                      );
                    }),
                  ],
                ),
                pw.SizedBox(height: 20),
                pw.Text(
                  "Total: \${_purchaseLineRepository.calculateListTotal(listId).toStringAsFixed(2)}",
                  style: pw.TextStyle(fontWeight: pw.FontWeight.bold),
                ),
              ],
            );
          },
        ),
      );

      // Save PDF
      final directory = await FilePicker.platform.getDirectoryPath();
      if (directory == null) return false;

      final file = File("$directory/shopping_list_${shoppingList.id}.pdf");
      await file.writeAsBytes(await pdf.save());
      return true;
    } catch (e) {
      print("Error exporting shopping list to PDF: $e");
      return false;
    }
  }
}
