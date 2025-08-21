# Deploy (Zero-Budget)

## GitHub Pages (Web)
1. Ensure repo on GitHub.
2. Build web:
   ```powershell
   flutter build web --release
   ```
3. Publish to `gh-pages` branch (one-time script; run from project root):
   ```powershell
   git worktree add gh-pages gh-pages
   robocopy .\build\web .\gh-pages /E
   cd gh-pages
   git add -A && git commit -m "deploy: web" && git push origin gh-pages
   ```
4. In GitHub repo Settings → Pages → set source to `gh-pages` branch.

> HTTPS is automatic on GitHub Pages. Camera access requires HTTPS.
