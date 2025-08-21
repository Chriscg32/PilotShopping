import 'package:flutter/services.dart';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';

class BarcodeScannerService {
  Future<String?> scanBarcode() async {
    try {
      final barcode = await FlutterBarcodeScanner.scanBarcode(
        '#FF6666',
        'Cancel',
        true,
        ScanMode.BARCODE,
      );

      // Return null if user canceled the scan
      if (barcode == '-1') return null;
      
      return barcode;
    } on PlatformException {
      return null;
    }
  }
}
