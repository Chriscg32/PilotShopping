import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

import 'ocr_service.dart';

/// Entry point of the application. The [main] function ensures that camera
/// initialization happens before the app runs. This is required by the
/// camera plugin.
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Obtain a list of the available cameras on the device. Cameras are needed
  // to provide a live preview for scanning price tags.
  final cameras = await availableCameras();
  runApp(PilotShoppingApp(cameras: cameras));
}

/// The root widget of the Quick Add MVP. This widget holds the list of
/// available cameras and passes them down to pages requiring access.
class PilotShoppingApp extends StatelessWidget {
  final List<CameraDescription> cameras;

  const PilotShoppingApp({Key? key, required this.cameras}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pilot Shopping',
      theme: ThemeData(
        primarySwatch: Colors.green,
        useMaterial3: true,
      ),
      home: HomePage(cameras: cameras),
    );
  }
}

/// The main page where users can see their running total, set a budget and
/// launch the scanner. It maintains internal state for the current total and
/// budget settings.
class HomePage extends StatefulWidget {
  final List<CameraDescription> cameras;
  const HomePage({Key? key, required this.cameras}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _totalCents = 0;
  int _budgetCents = 200000; // default budget: R2000.00
  int _alertGapCents = 50000; // alert threshold: R500.00

  /// Adds a price in cents to the running total. If the new total is within
  /// [_alertGapCents] of [_budgetCents], a snackbar alert is displayed.
  void _addPrice(int cents) {
    setState(() {
      _totalCents += cents;
    });
    if (_totalCents >= _budgetCents - _alertGapCents) {
      // Show warning that the budget threshold has been reached.
      final remaining = _budgetCents - _totalCents;
      final remainingText = (remaining / 100).toStringAsFixed(2);
      final thresholdText = (_alertGapCents / 100).toStringAsFixed(2);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Only R$remainingText remaining (threshold R$thresholdText).',
          ),
        ),
      );
    }
  }

  /// Presents a simple bottom sheet allowing the user to adjust their budget
  /// and alert gap. Values are stored in cents to avoid floating point
  /// precision issues.
  void _showBudgetSettings() {
    final budgetController = TextEditingController(
      text: (_budgetCents / 100).toStringAsFixed(2),
    );
    final alertController = TextEditingController(
      text: (_alertGapCents / 100).toStringAsFixed(2),
    );
    showModalBottomSheet(
      context: context,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Set Budget (R)', style: TextStyle(fontSize: 16)),
            TextField(
              controller: budgetController,
              keyboardType: const TextInputType.numberWithOptions(
                decimal: true,
              ),
              decoration: const InputDecoration(hintText: 'e.g. 2000.00'),
            ),
            const SizedBox(height: 12),
            const Text('Alert Threshold from Max (R)', style: TextStyle(fontSize: 16)),
            TextField(
              controller: alertController,
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              decoration: const InputDecoration(hintText: 'e.g. 500.00'),
            ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: () => Navigator.of(ctx).pop(),
                  child: const Text('Cancel'),
                ),
                ElevatedButton(
                  onPressed: () {
                    final budgetValue = double.tryParse(budgetController.text) ?? (_budgetCents / 100);
                    final alertValue = double.tryParse(alertController.text) ?? (_alertGapCents / 100);
                    setState(() {
                      _budgetCents = (budgetValue * 100).round();
                      _alertGapCents = (alertValue * 100).round();
                    });
                    Navigator.of(ctx).pop();
                  },
                  child: const Text('Save'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pilot Shopping'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: _showBudgetSettings,
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Total',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(
              'R${(_totalCents / 100).toStringAsFixed(2)}',
              style: Theme.of(context).textTheme.displayMedium,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                // Navigate to the scanner page and wait for result. The scanner
                // returns a price in cents if a price was confirmed, or null
                // otherwise.
                final priceCents = await Navigator.push<int?>(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ScannerPage(
                      cameras: widget.cameras,
                    ),
                  ),
                );
                if (priceCents != null) {
                  _addPrice(priceCents);
                }
              },
              child: const Text('Scan Price'),
            ),
          ],
        ),
      ),
    );
  }
}

/// A page that displays the camera preview and allows the user to scan a
/// price tag. The user must press a button to capture an image, after
/// which the OCR engine attempts to extract a price. If successful, a
/// confirmation dialog is shown allowing the user to add the price to
/// their total or cancel.
class ScannerPage extends StatefulWidget {
  final List<CameraDescription> cameras;
  const ScannerPage({Key? key, required this.cameras}) : super(key: key);

  @override
  State<ScannerPage> createState() => _ScannerPageState();
}

class _ScannerPageState extends State<ScannerPage> {
  CameraController? _cameraController;
  bool _processing = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  /// Initializes the first available camera. If no cameras are available,
  /// shows an error snackbar and pops this page.
  Future<void> _initializeCamera() async {
    if (widget.cameras.isEmpty) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No cameras available')),
        );
        Navigator.pop(context);
      });
      return;
    }
    final controller = CameraController(
      widget.cameras.first,
      ResolutionPreset.medium,
      enableAudio: false,
    );
    try {
      await controller.initialize();
    } catch (e) {
      // If initialization fails, notify user and pop.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to initialize camera: $e')),
        );
        Navigator.pop(context);
      });
      return;
    }
    if (mounted) {
      setState(() {
        _cameraController = controller;
      });
    }
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  /// Captures an image from the camera, performs OCR to extract a price,
  /// and shows a confirmation dialog. Returns the price in cents if
  /// confirmed, otherwise returns null.
  Future<void> _scanPrice() async {
    if (_processing) return;
    final controller = _cameraController;
    if (controller == null || !controller.value.isInitialized) return;
    setState(() {
      _processing = true;
    });
    try {
      final file = await controller.takePicture();
      final inputImage = InputImage.fromFilePath(file.path);
      final recognizer = TextRecognizer(script: TextRecognitionScript.latin);
      final recognizedText = await recognizer.processImage(inputImage);
      recognizer.close();
      // Parse price using helper function.
      final priceCents = OcrService.extractPrice(recognizedText.text);
      if (priceCents != null) {
        // Ask the user to confirm adding the price.
        final add = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            title: const Text('Price Found'),
            content: Text(
              'Add this price: R${(priceCents / 100).toStringAsFixed(2)}?',
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(ctx).pop(false),
                child: const Text('Cancel'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(ctx).pop(true),
                child: const Text('Add'),
              ),
            ],
          ),
        );
        if (add == true) {
          // Return the price to the caller.
          if (mounted) {
            Navigator.of(context).pop(priceCents);
          }
        }
      } else {
        // If no price found, show a message.
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No price detected. Try again.')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error scanning: $e')),
      );
    } finally {
      setState(() {
        _processing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final controller = _cameraController;
    return Scaffold(
      appBar: AppBar(title: const Text('Scan Price')),
      body: controller == null || !controller.value.isInitialized
          ? const Center(child: CircularProgressIndicator())
          : Stack(
              children: [
                Positioned.fill(
                  child: AspectRatio(
                    aspectRatio: controller.value.aspectRatio,
                    child: CameraPreview(controller),
                  ),
                ),
                if (_processing)
                  Positioned.fill(
                    child: Container(
                      color: Colors.black.withValues(alpha: 0.5),
                      alignment: Alignment.center,
                      child: const CircularProgressIndicator(),
                    ),
                  ),
              ],
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _scanPrice,
        child: const Icon(Icons.camera_alt),
      ),
    );
  }
}