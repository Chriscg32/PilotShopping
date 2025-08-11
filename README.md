# PilotShopping — Offline-First Shopping Budget & OCR Scanner

**Status:** Project bootstrap • **Date:** 2025-08-11

PilotShopping is a mobile app (Android-first) that lets you hover your phone over shelf **price tags** to capture the **price (and optionally item name)** using **on-device OCR**. It keeps a **running total**, enforces a **max budget with configurable alerts**, and (optionally) matches against a **shopping list**. It’s designed for **South African retail** realities (no scan-and-go, load-shedding, limited mobile data).

## Why offline-first?
- Works during **load-shedding** and without store Wi‑Fi.
- **Zero data** required for core features.
- Sync and receipt parsing are optional **Pro** features.

## Feature tiers
- **MVP**: OCR price → total, undo, budget + alert gap, receipt photo attach.
- **v1.1**: Shopping list + fuzzy name match; per‑kg toggle; exports (CSV/PDF).
- **Pro**: Cloud sync, receipt OCR on server, web dashboard, monthly exports, device sharing.

## Tech direction
- **Flutter** (recommended), camera + **Google ML Kit** Text Recognition (on-device).
- Local store: SQLite. Background sync queue when Pro enabled.
- Optional backend: Supabase (auth/storage/Postgres) or Firebase (auth/storage/Firestore).

## Quick start (Windows, zero-cost local setup)
1. Extract this repo to your PC.
2. (Optional) Run `scripts\windows\init_git.ps1` to initialize a Git repo and make the first commit.
3. Read `docs/PRD.md` then `docs/Architecture.md` to align requirements.
4. Decide initial build: **Quick Add MVP** vs **List Mode MVP** (see `docs/Roadmap.md`).

For GitHub publishing and pushing, see `docs/GitHub_Repo_Setup.md`.
