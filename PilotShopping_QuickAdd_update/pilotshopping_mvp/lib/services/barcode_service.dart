import 'package:mobile_scanner/mobile_scanner.dart';

class BarcodeService {
  final MobileScannerController _controller = MobileScannerController();

  MobileScannerController get controller => _controller;

  void startScanning() {
    _controller.start();
  }

  void stopScanning() {
    _controller.stop();
  }

  void toggleTorch() {
    _controller.toggleTorch();
  }

  void switchCamera() {
    _controller.switchCamera();
  }

  void dispose() {
    _controller.dispose();
  }
}
