# AI Agent Prompt Guide (Blackbox / ChatGPT-5)

## Operating Rules (Do Not Deviate)
1. Do not change dependency versions unless explicitly asked.
2. Preserve null-safety and avoid introducing `dynamic` where types are known.
3. Before writing code, list the plan and files to modify; then implement; then run a self-check.
4. Never remove error handling for camera permissions.
5. Keep code idempotent and deterministic; avoid "magic" global singletons.
6. After edits, generate a diff-style summary and list manual test steps.

## Common Pitfalls Guardrail
- Flutter Web camera: start scanning only after a user gesture; handle HTTPS requirement.
- Barcode scanning: do not assume barcodes contain price; always prompt user.
- State leaks: cancel controllers/streams on `dispose()`; guard `setState` after unmount.
- Time/locale: use `intl` for currency; never string-concatenate for money.
- File exports on web: use `AnchorElement(href: blobUrl)`; revoke URLs after download.

## Definition of Done
- All acceptance criteria in PRD satisfied for the task scope.
- `flutter analyze` clean; tests pass; manual test notes included.
- Docs updated (CHANGELOG, when appropriate).
