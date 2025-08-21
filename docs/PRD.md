# Product Requirements Document (PRD) — PilotShopping MVP

## 1. Summary
PilotShopping helps shoppers build a checklist and mark items as purchased by scanning the product barcode with the phone/web camera. It tracks quantity and price per purchase, warns when approaching a session budget, exports to CSV/PDF, and automatically learns monthly favorites. MVP is **offline-first** and **zero-budget**: no paid APIs; optional cloud sync deferred.

## 2. Goals
- ✅ Create shopping lists with checkboxes and quantities.
- ✅ Scan product barcodes to identify items and mark them purchased.
- ✅ Capture price and quantity at the moment of purchase; update running subtotal.
- ✅ Favorites & recurring list (month-to-month carryover / frequent items).
- ✅ Budget guardrail: max budget per session + pre-threshold warning (e.g., when ≤ $500 remaining).
- ✅ Export data to CSV and PDF.
- ✅ Store and retrieve receipt snapshots and till-slip barcodes.
- ✅ Run on the web (mobile browser) with camera support (HTTPS required).

## 3. Non-Goals (MVP)
- ✗ Live price comparison across retailers.
- ✗ Cloud sync (Google Sheets / Excel online / vendor APIs).
- ✗ Native Android/iOS releases (web first), Windows packaging later.
- ✗ OCR of receipts (we store images + barcodes; OCR is a later phase).

## 4. Users & Jobs To Be Done
- **Primary Shopper**: "I want a quick way to check off items and track spend as I shop."
- **Budget-conscious parent/student**: "Warn me before I blow my budget."
- **Record-keeper**: "Keep receipts and prices for returns or tax tracking."

## 5. Key User Stories (Acceptance Criteria)
1. **Create List**: As a user, I can add items (name, optional notes). *AC:* I see a list with items and unchecked boxes.
2. **Scan to Check Off**: As a user, I can use the camera to scan a barcode; if the item exists, it's checked and quantity defaults to 1. *AC:* Item status becomes purchased, and subtotal updates after price entry.
3. **Price & Quantity**: After scanning, I can edit quantity (default 1) and enter the price. *AC:* Price * quantity contributes to subtotal; stored in local DB with timestamp.
4. **Budget Warning**: I can set a max budget and an early warning threshold (e.g., warn when ≤ $500 remaining). *AC:* Toast/bottom-sheet alert triggers appropriately.
5. **Favorites/Recurring**: The app suggests a monthly default list based on past purchases (frequency). *AC:* I can generate this list at month start.
6. **Receipts & Till Slip**: I can capture a photo of the receipt and (optionally) scan receipt barcode; both are stored locally and linked to the session. *AC:* I can view the receipt later.
7. **Exports**: I can export purchases to CSV and PDF. *AC:* A file downloads with line items, totals, and date range.
8. **What's Left**: I can see outstanding items (not yet purchased) at any time. *AC:* Filter "Outstanding" shows remaining items count.

## 6. Functional Requirements
- **List Management**: CRUD lists & items; per-item fields { name, barcode(s), notes, lastPrice, favoriteFlag }.
- **Scanning**: Supports EAN/UPC/Code-128 on web via camera; maps barcode → item if known; otherwise offers create-item with barcode prefilled.
- **Purchases**: Each scan creates/updates a **PurchaseLine** { itemId, qty, unitPrice, total, timestamp, listId }.
- **Budget**: Session budget and warnThreshold; compute subtotal/live remaining.
- **Favorites**: Auto-favorite when purchased ≥ N times in last M months (defaults: N=2, M=2) — tunable.
- **Export**: CSV and PDF for a date range or current session/list.
- **Receipts**: Attach image and decoded receipt barcode string (if present) to the session; multiple receipts allowed.
- **Offline-first storage**: All data local; import/export JSON for backups.

## 7. Non-Functional Requirements
- Works offline after initial load (PWA capable on Flutter web).
- Smooth scanning UX (< 1s feedback on modern phones, conditions permitting).
- Local data durability across app restarts.
- Privacy: data never leaves the device unless user exports/shares.

## 8. Platform Scope (MVP)
- **Target**: Web (Chrome/Edge/Firefox mobile where camera supported; iOS Safari requires HTTPS).
- **Next**: Windows desktop after Visual Studio install.

## 9. Risks / Mitigations
- **Camera permissions on iOS Safari**: Use HTTPS (GitHub Pages) and user gesture to start camera; show manual entry fallback.
- **Barcode data rarely contains price**: Always prompt user for price on purchase; maintain price history.
- **Web local storage limits**: Keep images reasonable; allow periodic export & delete of old receipts.

## 10. Success Metrics
- Time to first scan < 60s from first load.
- ≥ 80% lists have at least one scan-completed item.
- Export used by ≥ 30% active users monthly.

## 11. Release Criteria
- All acceptance tests green; manual test plan passed.
- Lighthouse PWA passes basic checks.
- No crash repro in smoke scenarios (create→scan→edit qty/price→export).
