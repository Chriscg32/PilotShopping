# Port Conflict Resolution Script
Write-Host "🔧 Fixing Port Conflicts..." -ForegroundColor Cyan

# Find what's using port 8000
Write-Host "`n🔍 Checking port 8000..." -ForegroundColor Yellow
$port8000 = netstat -ano | findstr :8000
if ($port8000) {
    Write-Host "Port 8000 is in use:" -ForegroundColor Red
    $port8000 | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    
    # Get all containers using port 8000
    $containers = docker ps --filter "publish=8000" --format "table {{.Names}}\t{{.Ports}}"
    if ($containers) {
        Write-Host "`nContainers using port 8000:" -ForegroundColor Yellow
        $containers | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
        
        # Stop conflicting containers
        Write-Host "`n🛑 Stopping conflicting containers..." -ForegroundColor Yellow
        docker ps --filter "publish=8000" --format "{{.Names}}" | ForEach-Object {
            if ($_ -ne "butterflyblue-app") {
                Write-Host "  Stopping: $_" -ForegroundColor Red
                docker stop $_
                docker rm $_
            }
        }
    }
}

# Clean up any orphaned containers
Write-Host "`n🧹 Cleaning up orphaned containers..." -ForegroundColor Yellow
docker container prune -f

# Restart our app service
Write-Host "`n🚀 Starting ButterflyBlue app..." -ForegroundColor Cyan
docker-compose up -d app

# Wait for app to start
Write-Host "`n⏳ Waiting for app to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Test the application
Write-Host "`n🧪 Testing application..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Application is healthy!" -ForegroundColor Green
        Write-Host "🌐 Available at: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "❌ Application health check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "📋 Checking logs..." -ForegroundColor Yellow
    docker-compose logs app --tail=20
}

# Final status
Write-Host "`n📊 Current Status:" -ForegroundColor Blue
docker-compose ps