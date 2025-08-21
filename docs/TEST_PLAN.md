# Test Plan — MVP

## Smoke
- Launch app on Chrome (HTTPS), grant camera.
- Create list, add 3 items manually.
- Scan barcode for known item → auto check, qty=1, enter price → subtotal updates.
- Edit qty to 3 → subtotal reflects 3×.
- Set budget=1500, warnThreshold=500; simulate scans/prices until warning triggers.
- Mark all items → "All purchased" prompt visible.
- View Outstanding filter shows remaining when not all purchased.
- Export CSV and PDF; open files and verify totals.
- Attach a receipt image and scan its barcode; reopen session to view.
