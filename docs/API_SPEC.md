# API Spec (Pro, Optional)

`POST /sync`
- Headers: Authorization bearer token (anon or email auth)
- Body: `{ device_id, last_sync_at, changes: [{entity, entity_id, op, payload, last_modified}] }`
- Response: `{ applied: [...], conflicts: [...], server_time }`

`POST /receipts`
- Multipart: image + metadata
- Response: `{ receipt_id, image_url, ocr_status }`

`GET /trips/:id` etc. (standard CRUD)
