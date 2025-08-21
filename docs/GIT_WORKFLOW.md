# Git Workflow

## First-Time Setup
```powershell
# inside project root
git init
git remote add origin https://github.com/<your-username>/PilotShopping.git
# if you already have a repo, just set origin and pull
```

## Typical Cycle

```powershell
# update local
git checkout main
git pull --rebase origin main

# new work
git checkout -b feat/scan-purchase-flow
# ... make changes ...
git add -A
git commit -m "feat: implement scan→qty→price purchase flow"

git push -u origin feat/scan-purchase-flow
# open PR, merge via GitHub, then

git checkout main
git pull --rebase origin main
```

## Releases

- Tag: `git tag v0.1.0 && git push --tags`
- Update CHANGELOG for each release.
