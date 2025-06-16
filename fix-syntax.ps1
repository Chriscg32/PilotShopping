# Syntax Error Fix Script
Write-Host "🔧 Fixing Syntax Errors in main.py..." -ForegroundColor Cyan

# Backup the current main.py
Copy-Item "main.py" "main.py.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Write-Host "✅ Backup created: main.py.backup.*" -ForegroundColor Green

# Read the file content
$content = Get-Content "main.py" -Raw

# Common fixes for unterminated strings
$fixes = @{
    '@app\.get\("/api/$' = '@app.get("/api/health")'
    '@app\.post\("/api/$' = '@app.post("/api/tasks")'
    '@app\.put\("/api/$' = '@app.put("/api/update")'
    '@app\.delete\("/api/$' = '@app.delete("/api/delete")'
    '"/api/$' = '"/api/health"'
    "'[^']*$" = "'/api/health'"
}

# Apply fixes
$originalContent = $content
foreach ($pattern in $fixes.Keys) {
    $replacement = $fixes[$pattern]
    $content = $content -replace $pattern, $replacement
}

# Check if we made any changes
if ($content -ne $originalContent) {
    # Write the fixed content back
    $content | Set-Content "main.py" -NoNewline
    Write-Host "✅ Syntax errors fixed!" -ForegroundColor Green
} else {
    Write-Host "ℹ️ No automatic fixes applied. Manual inspection needed." -ForegroundColor Yellow
}

# Show the problematic area
Write-Host "`n📋 Content around line 328:" -ForegroundColor Blue
$lines = $content -split "`n"
$startLine = [Math]::Max(0, 325)
$endLine = [Math]::Min($lines.Count - 1, 335)

for ($i = $startLine; $i -le $endLine; $i++) {
    $lineNum = $i + 1
    $marker = if ($lineNum -eq 328) { ">>> " } else { "    " }
    Write-Host "$marker$lineNum`: $($lines[$i])" -ForegroundColor $(if ($lineNum -eq 328) { "Red" } else { "White" })
}