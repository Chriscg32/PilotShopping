import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class BarcodeScannerWidget extends StatefulWidget {
  final Function(String) onBarcodeDetected;
  final VoidCallback onClose;

  const BarcodeScannerWidget({
    Key? key,
    required this.onBarcodeDetected,
    required this.onClose,
  }) : super(key: key);

  @override
  State<BarcodeScannerWidget> createState() => _BarcodeScannerWidgetState();
}

class _BarcodeScannerWidgetState extends State<BarcodeScannerWidget> {
  late MobileScannerController controller;
  bool isFlashOn = false;
  bool isFrontCamera = false;

  @override
  void initState() {
    super.initState();
    controller = MobileScannerController(
      detectionSpeed: DetectionSpeed.normal,
      facing: CameraFacing.back,
      torchEnabled: false,
    );
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Scan Barcode"),
        actions: [
          IconButton(
            icon: Icon(isFlashOn ? Icons.flash_on : Icons.flash_off),
            onPressed: () async {
              await controller.toggleTorch();
              setState(() {
                isFlashOn = !isFlashOn;
              });
            },
          ),
          IconButton(
            icon: Icon(isFrontCamera ? Icons.camera_front : Icons.camera_rear),
            onPressed: () async {
              await controller.switchCamera();
              setState(() {
                isFrontCamera = !isFrontCamera;
              });
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: controller,
            onDetect: (capture) {
              final List<Barcode> barcodes = capture.barcodes;
              if (barcodes.isNotEmpty) {
                final String? code = barcodes.first.rawValue;
                if (code != null) {
                  widget.onBarcodeDetected(code);
                }
              }
            },
          ),
          // Overlay with scanning area indicator
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.white,
                  width: 2.0,
                ),
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          // Instruction text
          Positioned(
            bottom: 40,
            left: 0,
            right: 0,
            child: Center(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Text(
                  "Position the barcode within the frame",
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
