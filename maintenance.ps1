# ButterflyBlue Creations - Maintenance Script
param(
    [switch]$CleanLogs,
    [switch]$BackupData,
    [switch]$UpdateImages,
    [switch]$RestartServices,
    [switch]$FullMaintenance
)

Write-Host "🔧 ButterflyBlue Maintenance Tools" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

if ($FullMaintenance -or $CleanLogs) {
    Write-Host "`n🧹 Cleaning logs..." -ForegroundColor Yellow
    
    # Clean Docker logs
    docker system prune -f
    
    # Clean application logs
    if (Test-Path "logs") {
        Get-ChildItem "logs" -Filter "*.log" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item -Force
        Write-Host "✅ Old log files cleaned" -ForegroundColor Green
    }
}

if ($FullMaintenance -or $BackupData) {
    Write-Host "`n💾 Backing up data..." -ForegroundColor Yellow
    
    $backupDir = "backups/$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    # Backup database
    try {
        docker exec butterflyblue-postgres pg_dump -U butterflyblue_user -d butterflyblue > "$backupDir/database.sql"
        Write-Host "✅ Database backup created" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Database backup failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Backup application data
    if (Test-Path "data") {
        Copy-Item -Path "data" -Destination "$backupDir/app-data" -Recurse -Force
        Write-Host "✅ Application data backup created" -ForegroundColor Green
    }
    
    # Backup configuration
    Copy-Item -Path "config" -Destination "$backupDir/config" -Recurse -Force
    Write-Host "✅ Configuration backup created" -ForegroundColor Green
    
    Write-Host "📁 Backup saved to: $backupDir" -ForegroundColor Cyan
}

if ($FullMaintenance -or $UpdateImages) {
    Write-Host "`n🔄 Updating Docker images..." -ForegroundColor Yellow
    
    docker-compose pull
    Write-Host "✅ Images updated" -ForegroundColor Green
}

if ($FullMaintenance -or $RestartServices) {
    Write-Host "`n🔄 Restarting services..." -ForegroundColor Yellow
    
    docker-compose restart
    
    # Wait for services to be ready
    Start-Sleep -Seconds 30
    
    # Health check
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Services restarted successfully" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "⚠️ Services may still be starting up" -ForegroundColor Yellow
    }
}

# System health report
Write-Host "`n📊 System Health Report:" -ForegroundColor Blue

# Disk usage
$diskUsage = Get-WmiObject -Class Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3}
foreach ($disk in $diskUsage) {
    $freePercent = [math]::Round(($disk.FreeSpace / $disk.Size) * 100, 2)
    $status = if ($freePercent -gt 20) { "✅" } else { "⚠️" }
    Write-Host "  $status Disk $($disk.DeviceID) - Free: $freePercent%" -ForegroundColor $(if ($freePercent -gt 20) { "Green" } else { "Yellow" })
}

# Docker system info
try {
    $dockerInfo = docker system df --format "table {{.Type}}\t{{.Total}}\t{{.Active}}\t{{.Size}}\t{{.Reclaimable}}" | Select-Object -Skip 1
    Write-Host "`n🐳 Docker Resource Usage:" -ForegroundColor Blue
    foreach ($line in $dockerInfo) {
        if ($line.Trim()) {
            Write-Host "  📊 $line" -ForegroundColor White
        }
    }
}
catch {
    Write-Host "❌ Unable to get Docker system info" -ForegroundColor Red
}

Write-Host "`n🎉 Maintenance completed!" -ForegroundColor Green