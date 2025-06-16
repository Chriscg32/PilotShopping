# ButterflyBlue Complete Fix Script
Write-Host "🔧 Comprehensive ButterflyBlue Fix..." -ForegroundColor Cyan

# Step 1: Stop all containers
Write-Host "`n🛑 Stopping all containers..." -ForegroundColor Yellow
docker-compose down -v
docker stop ai-saas-mosquitto ai-saas-n8n ai-saas-qdrant landing-copy-generator-prometheus-1 2>$null

# Step 2: Clean up
Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
docker system prune -f
docker volume prune -f

# Step 3: Ensure directories exist
Write-Host "📁 Creating required directories..." -ForegroundColor Yellow
$dirs = @("init", "config", "logs", "data", "backups")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created $dir directory" -ForegroundColor Green
    }
}

# Step 4: Build and start services
Write-Host "`n🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d --build

# Step 5: Wait for services to be ready
Write-Host "`n⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

# Step 6: Check service health
Write-Host "`n🏥 Checking service health..." -ForegroundColor Blue

$services = @(
    @{Name="PostgreSQL"; Command="docker exec butterflyblue-postgres pg_isready -U butterflyblue_user -d butterflyblue"},
    @{Name="Redis"; Command="docker exec butterflyblue-redis redis-cli -a butterflyblue123 ping"},
    @{Name="Application"; Command="curl -f http://localhost:8000/health"}
)

foreach ($service in $services) {
    try {
        $result = Invoke-Expression $service.Command 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $($service.Name): Healthy" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($service.Name): Unhealthy" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  ❌ $($service.Name): Error - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Step 7: Test database connection
Write-Host "`n🗄️ Testing database..." -ForegroundColor Blue
try {
    $dbTest = docker exec butterflyblue-postgres psql -U butterflyblue_user -d butterflyblue -c "SELECT COUNT(*) FROM agents;" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Database tables created successfully" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Database test failed" -ForegroundColor Red
    }
}
catch {
    Write-Host "  ❌ Database connection error" -ForegroundColor Red
}

# Step 8: Final status check
Write-Host "`n📊 Final Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host "`n🎉 Fix completed!" -ForegroundColor Green
Write-Host "🌐 Application should be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "📊 Monitoring: http://localhost:3000 (admin/admin123)" -ForegroundColor Cyan