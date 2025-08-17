# Data Model

## Tables
### Trip
- id (uuid), user_id, store_name?, store_branch?  
- started_at, ended_at?, budget_cents, alert_gap_cents, total_cents, currency='ZAR'  
- status ('open'|'closed'), device_id, last_modified (UTC)

### TripItem
- id, trip_id, name, price_cents, qty (int, default 1)  
- source ('ocr'|'manual'|'barcode'), unit ('each'|'kg'|'L'|'other')  
- notes?, created_at, last_modified

### Receipt
- id, trip_id, image_uri_local, image_uri_cloud?, image_hash  
- till_barcode?, number?, date?, total_cents?, vat_cents?, parsed_json?  
- created_at, last_modified

### SyncQueue
- id, entity, entity_id, op ('upsert'|'delete'), payload_json, retries, last_try_at

## Indexing
- By trip_id for TripItem, by user_id for Trip, by last_modified for sync.
