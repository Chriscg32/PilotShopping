# Architecture — PilotShopping MVP

## Tech Stack
- **Flutter 3.35.x / Dart 3.9** (single codebase; web first)
- **Packages (MVP)**
  - Scanning: `mobile_scanner` (web/Android/iOS) — used on web for camera scanning
  - Local DB: `hive`, `hive_flutter`
  - Paths: `path_provider` (non-web usages later), `universal_html` as needed
  - Export: `csv`, `pdf`, `printing` (for local print/share, optional)
  - Utils: `intl`, `uuid`

> Note: Windows desktop scanning via webcam is not part of MVP. For desktop later, keep manual entry or evaluate native plugins.

## High-Level Modules
- **domain/**: pure models & business rules
  - `Item`, `ShoppingList`, `PurchaseLine`, `Session`, `PriceHistory`, `Receipt`
- **data/**: persistence & repositories
  - Hive boxes: `items`, `lists`, `purchases`, `receipts`, `settings`
  - `ItemRepository`, `ListRepository`, `PurchaseRepository`, `ReceiptRepository`, `SettingsRepository`
- **services/**: cross-cutting capabilities
  - `ScannerService` (wrap `mobile_scanner`)
  - `ExportService` (CSV/PDF)
  - `FavoritesService` (frequency analysis)
- **ui/**: Flutter screens & state
  - `HomeScreen`, `ListDetailScreen`, `ScanScreen`, `BudgetBanner`, `OutstandingScreen`, `ExportsScreen`, `SettingsScreen`
  - State management: start with `ValueNotifier`/`ChangeNotifier`; upgradeable to BLoC/Riverpod later.

## Data Model (core)
- **Item**: { id, name, barcodes: List<String>, notes, lastPrice, favoriteFlag }
- **ShoppingList**: { id, name, monthKey, itemIds: List<String> }
- **PurchaseLine**: { id, listId, itemId, qty, unitPrice, total, timestamp }
- **Receipt**: { id, listId, imageRef, receiptBarcode }
- **Settings**: { sessionBudget, warnThreshold }

## Storage
- Hive keys per collection; versioned adapters.
- Image storage
  - Web: store in IndexedDB via `hive` as bytes or use `url` from `FileReader` and save as blobs; keep sizes small.
  - Desktop/mobile (later): save to app data dir (via `path_provider`) and store file path in Hive.

## Exports
- **CSV**: columns [date, listName, itemName, barcode, qty, unitPrice, total]
- **PDF**: one page per session or list, summary totals, optional receipt thumbnails.

## Security & Privacy
- No external network calls in MVP.
- All data local unless user exports a file.

## Feature Flags
- `enableDesktopScan` (default false)
- `enableCloudSync` (future)
- `enablePriceCompare` (future)
