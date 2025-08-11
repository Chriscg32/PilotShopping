# GitHub Repo Setup

## Option A — Website (no CLI)
1. Create a new repo at github.com (e.g., `PilotShopping`), **Public**.
2. On your PC, open PowerShell in the project folder.
3. Run:
```
git init
git add .
git commit -m "chore: bootstrap PilotShopping starter"
git branch -M main
git remote add origin https://github.com/<YOUR-USER>/PilotShopping.git
git push -u origin main
```

## Option B — GitHub CLI (if installed)
```
git init
gh repo create PilotShopping --public --source=. --remote=origin --push
```

If two-factor or PAT is required, follow GitHub prompts.
