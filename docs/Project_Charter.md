# Project Charter — PilotShopping

**Date:** 2025-08-11  
**Project Lead:** You (with AI co-pilot)  
**Vision:** Give South African shoppers a reliable, offline, camera-powered **budget companion** that prevents overspending in-store without relying on the retailer.

## Objectives & Success Metrics
- **O1**: MVP live to early testers (APK sideload) within 4 weeks.  
- **O2**: 90%+ scans correctly parsed (price) in normal lighting.  
- **O3**: ≥70% of testers report reduced overspend vs baseline.  
- **O4**: Pro conversion ≥5% by month 2 (cloud sync + receipts OCR).

## Scope (MVP)
- OCR price capture → running total.
- Budget setting + alert gap.
- Receipt photo capture (no parsing).
- Exports: CSV of trip.

**Out of scope (MVP)**: Store integrations, online payment, loyalty integration.

## Stakeholders
- **Founder/Product**: Vision, prioritization, GTM.
- **Engineering (Mobile)**: Flutter development, OCR pipeline, storage.
- **Backend (Pro)**: Sync API, storage, receipt OCR parsing.
- **Design/UX**: Flows, accessibility, visual design.
- **QA**: Device testing, low-light, glare, edge tags.
- **Legal/Privacy**: Policies, consent, data handling.
- **Support/Community**: Docs, bug triage, feedback loop.

## Risks (Top 5)
1. OCR misreads under glare — *Mitigation*: pre-processing + confirm/undo UI.  
2. Per‑kg vs per‑item confusion — *Mitigation*: explicit toggle; unit parsing.  
3. Battery drain — *Mitigation*: throttle frame analysis; pause on motion.  
4. Data loss concerns — *Mitigation*: local backups; Pro sync optional.  
5. Play Store fees — *Mitigation*: zero-cost launch via APK + closed testing first.
