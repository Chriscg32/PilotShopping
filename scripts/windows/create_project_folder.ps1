param(
  [string]$TargetPath = "C:\Users\chris\OneDrive\Documentos\PilotShopping"
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path $TargetPath)) {
  New-Item -ItemType Directory -Path $TargetPath | Out-Null
}

# Suggestion: Extract the downloaded ZIP here.
Write-Host "Created $TargetPath. Please extract the downloaded 'PilotShopping_starter.zip' into this folder." -ForegroundColor Green
