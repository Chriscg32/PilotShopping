# PilotShopping — PRD v2
Goal: Offline-first total tracker with OCR, bulk & per-kg items, and currency by device locale (ZAR in ZA, USD in US). Local SQLite; CSV export. Pro later: cloud sync, receipts OCR, family sharing.

MVP v2 Must-haves
- OCR → confirm → edit/undo
- Bulk per-unit: quantity × unit price
- Per-kg: price/kg × weight (store weight in grams; cents for money)
- Budget + alert gap; optional hard stop
- Currency auto-detect by device locale; user override
- Shopping list with mark-off + monthly repeats
- CSV export; fully offline

Acceptance
- 66 × R12.50 = R825.00 (bulk)
- R79.99/kg × 5.00 kg = R399.95 (per-kg)
- Locale-correct currency display; override persists
- Works offline; no crashes when offline

Data Model (SQLite)
Trip(id, started_at, ended_at?, budget_cents, alert_gap_cents, total_cents, currency_code)
TripItem(id, trip_id, name, unit in {each,kg}, quantity, weight_grams, unit_price_cents, price_basis in {unit,per_kg}, line_total_cents, source, created_at)
Settings(id=1, currency_code, locale, use_biometric, pin_hash?)

UX Flows
Home: total, budget bar, items, Undo
Scan: camera → confirm sheet (Unit Each/Per kg, Quantity or Weight kg) → line total preview → Confirm
List Mode: mark-off scanned items; re-use last month’s list (remove/add)
Settings: currency auto/override, budget presets, biometric lock

Risks
OCR misreads (mitigate via confirm), per-kg confusion (explicit toggle), locale edge cases (manual override), load shedding (local-first).
