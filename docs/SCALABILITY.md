# Scalability Plan (Post-Profit)

- **Data**: migrate from Hive to a cloud-synced store (e.g., Firestore/Supabase) while keeping offline cache.
- **Sync**: background sync on sign-in; conflict resolution by timestamp + last-write-wins.
- **Price Compare**: per-retailer ingestion via public endpoints or partner feeds; normalize by GTIN/EAN.
- **Receipts OCR**: on-device OCR for totals + vendor; privacy-first.
- **Modularity**: keep domain/services isolated to swap storage/scan impls without UI rewrites.
