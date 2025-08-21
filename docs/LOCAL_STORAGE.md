# Local Storage & Backups

## Storage Engine
- **Hive** boxes:
  - `items`, `lists`, `purchases`, `receipts`, `settings`

## Images & Receipts
- **Web**: store small image blobs in Hive or maintain object URLs; restrict size (e.g., compress to ≤ 300KB).
- **Desktop/mobile (later)**: save to app data dir (via `path_provider`) and store file path in Hive.

## Backups
- Export JSON (settings + all collections) periodically.
- CSV/PDF exports are for reporting; JSON is the authoritative backup.
