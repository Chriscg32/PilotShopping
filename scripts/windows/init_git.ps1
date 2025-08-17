param(
  [string]$RepoPath = ".",
  [string]$InitialMessage = "chore: bootstrap PilotShopping starter"
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $RepoPath
if (-not (Test-Path ".git")) {
  git init
}
git add .
git commit -m $InitialMessage
git branch -M main
Write-Host "Initialized git repo and made first commit on 'main'." -ForegroundColor Green
Pop-Location
