# Pilot Shopping Quick Add MVP

This directory contains a minimal Flutter prototype for the **Pilot Shopping**
application. The goal of this MVP is to demonstrate on‑device price scanning
and budget tracking without any server dependencies. It implements the
"Quick Add" flow described in the product architecture:

* Capture an image of a shelf price tag using the device camera.
* Run on‑device OCR (via Google ML Kit) to recognise the printed price.
* Parse the recognised text to extract a currency amount.
* Ask the user to confirm adding the price to the running total.
* Maintain a simple budget and alert threshold.

## Getting Started

> **Prerequisites**: Flutter 3.x, Android Studio or Xcode with emulators or
> physical devices, and the **google_mlkit_text_recognition** plugin. This
> project is set up for an offline‑first experience and does not require
> network connectivity.

1. Ensure you have a Flutter environment set up on your machine. See
   [flutter.dev/docs/get-started/install](https://flutter.dev/docs/get-started/install).
2. Navigate to this directory:

   ```sh
   cd PilotShopping_QuickAdd
   ```

3. Fetch the dependencies:

   ```sh
   flutter pub get
   ```

4. Run the application on an emulator or device:

   ```sh
   flutter run
   ```

5. The app opens to a home page showing your running total. Use the
   **settings** icon to adjust your budget and alert gap. Tap **Scan Price**
   to open the camera. After aligning the price tag and pressing the
   camera button, confirm the detected price to add it to your total.

## File Structure

* `pubspec.yaml` – project manifest declaring dependencies.
* `lib/main.dart` – entry point and user interface. Contains the home page
  and scanning flow.
* `lib/ocr_service.dart` – helper class for parsing prices from recognised
  text.
* `README.md` – this documentation.

## Extending This Prototype

This MVP focuses solely on scanning and summing prices. For a full
production release, consider implementing the following features:

* **Persistent storage** of trips and scanned items using `sqflite`.
* **Shopping list mode** with fuzzy matching of item names.
* **Cloud sync** and optional server‑side receipt processing.
* **Weight handling** for per‑kilogram pricing.
* **Accessibility enhancements** such as voice prompts and larger fonts.

Contributions and feedback are welcome. Open issues or pull requests on
GitHub to discuss improvements.
