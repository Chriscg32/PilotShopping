# Product Requirements Document (PRD) — PilotShopping

## Problem
South African shoppers often lack self-checkout and have connectivity issues. Manually totalling with a calculator is slow and error-prone.

## Users
- **Primary**: Budget-conscious shoppers; limited mobile data; Android-first.
- **Secondary**: Families tracking monthly grocery spend; returns management.

## Jobs-to-be-done
- *When shopping*, I want to **scan prices quickly** so I keep a correct running total.
- *When nearing my budget*, I want a **clear alert** so I can swap items.
- *After checkout*, I want to **store my receipt** for returns and monthly tracking.

## Core Requirements (MVP)
1. **Scan price tag** with camera; OCR extracts price (and optionally name).  
2. **Running total** updates instantly; show list of items.  
3. **Budget**: set max; customizable **alert gap** (e.g., R500).  
4. **Undo / Edit** last item; manual keypad fallback.  
5. **Receipt photo** attach (gallery + camera).  
6. **Exports**: CSV per trip.

### Non-functional
- Works fully **offline**; <150ms OCR-to-add on mid-tier Android.  
- Battery-friendly: throttled analysis; pause on motion.  
- Accessibility: large text mode, haptics, high-contrast theme.

## Deferred (v1.1+)
- Shopping list with fuzzy match and mark-off.  
- Per‑kg flow (enter weight).  
- Pro cloud sync & receipt OCR; web dashboard.  
- Family sharing; categories; monthly budget & reports.

## Acceptance Criteria (MVP)
- ≥90% price read success on standard tags in good light.  
- End-to-end trip flow w/ export CSV tested on 5 common Android devices.  
- Budget alert triggers at correct threshold (unit tests + manual E2E).

## Metrics
- Time-to-first-scan; scans/session; undo rate; alert rate; export usage; retention (D7/D30).
