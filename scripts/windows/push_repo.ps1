param(
  [string]$RepoPath = ".",
  [string]$RemoteUrl = ""
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RemoteUrl)) {
  Write-Error "RemoteUrl is required. Example: https://github.com/<USER>/PilotShopping.git"
  exit 1
}

Push-Location $RepoPath
if (-not (Test-Path ".git")) {
  git init
  git add .
  git commit -m "chore: bootstrap PilotShopping starter"
  git branch -M main
}
git remote remove origin 2>$null
git remote add origin $RemoteUrl
git push -u origin main
Pop-Location
Write-Host "Pushed to $RemoteUrl" -ForegroundColor Green
