# PilotShopping MVP

A shopping list app to help you manage your shopping needs efficiently.

## Features

- Create and manage shopping lists
- Add, edit, and delete items
- Track purchases with receipts
- Scan barcodes to quickly add items
- Export data to CSV and PDF formats
- Dark mode support
- Multiple currency support

## Project Structure

```
lib/
 data/           # Data layer (repositories, local storage)
 domain/         # Domain layer (models, business logic)
 services/       # Services (barcode scanning, export)
 ui/             # UI layer
    screens/    # App screens
    theme/      # App theme
    widgets/    # Reusable widgets
 main.dart       # App entry point
```

## Getting Started

1. Clone the repository
2. Run `flutter pub get` to install dependencies
3. Run `flutter pub run build_runner build` to generate Hive adapters
4. Run `flutter run` to start the app

## Dependencies

- flutter: Flutter SDK
- hive & hive_flutter: Local database
- provider: State management
- intl: Internationalization
- uuid: Unique ID generation
- path_provider: File system access
- image_picker: Image selection
- mobile_scanner: Barcode scanning
- photo_view: Image viewing
- file_picker: File selection
- pdf & csv: Export functionality
- share_plus: Sharing functionality
- flutter_slidable: Swipe actions
- fl_chart: Charts and graphs
