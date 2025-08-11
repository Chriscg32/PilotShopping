# Architecture — Offline-first with Optional Cloud

## Mobile
- **Flutter** app, on-device OCR via Google ML Kit.
- Local DB: SQLite (`sqflite`), Outbox pattern for future sync.
- Services: Camera → Preprocess → OCR → Parse → Confirm → Add.

## Data Model
See `docs/Data_Model.md`.

## Sync (Pro tier)
- Auth: anonymous → optional email/PIN.
- Endpoints: `/sync` for batched changes; LWW conflict resolution.
- Storage: Postgres (Supabase) or Firestore; receipts in S3-compatible storage.

## OCR Pipeline
1) ROI crop → grayscale → adaptive threshold → sharpen → deskew.  
2) Text recognition (on-device).  
3) Parse: regex for price; heuristic for largest number; optional name line.  
4) Confirm/undo UI; dedupe same-price within short interval.

## Performance
- Analyze every N frames; stop when device moving.  
- Cache last successful exposure/focus settings where supported.
