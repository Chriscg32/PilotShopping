# ButterflyBlue Creations - Production Launch Script (PowerShell)
param(
    [string]$Environment = "production",
    [string]$Version = "latest",
    [bool]$BackupEnabled = $true
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

function Write-Log {
    param([string]$Message, [string]$Color = "White")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

Write-Host "🦋 ButterflyBlue Creations - Production Launch" -ForegroundColor $Blue
Write-Host "==================================================" -ForegroundColor $Blue
Write-Host "Environment: $Environment"
Write-Host "Version: $Version" 
Write-Host "Backup Enabled: $BackupEnabled"
Write-Host "==================================================" -ForegroundColor $Blue

# Pre-flight checks
Write-Log "🔍 Running pre-flight checks..." $Blue

# Check required tools
$requiredTools = @("docker", "docker-compose", "curl")
foreach ($tool in $requiredTools) {
    if (!(Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Log "❌ Required tool not found: $tool" $Red
        exit 1
    }
}

Write-Log "✅ Pre-flight checks passed" $Green

# Set environment variables if not set
if (!$env:JWT_SECRET_KEY) {
    $env:JWT_SECRET_KEY = [System.Web.Security.Membership]::GeneratePassword(32, 0)
    Write-Log "⚠️ JWT_SECRET_KEY generated automatically" $Yellow
}

# Deploy application
Write-Log "🚀 Deploying ButterflyBlue Creations..." $Blue

# Stop existing services gracefully
Write-Log "Stopping existing services..."
docker-compose down --timeout 30

# Start new deployment
Write-Log "Starting new deployment..."
docker-compose up -d --build

# Wait for services to be ready
Write-Log "⏳ Waiting for services to be ready..." $Blue
Start-Sleep -Seconds 30

# Health check loop
$maxRetries = 30
$retryCount = 0

while ($retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ Application is healthy" $Green
            break
        }
    }
    catch {
        # Continue with retry logic
    }
    
    $retryCount++
    Write-Log "Health check attempt $retryCount/$maxRetries..."
    Start-Sleep -Seconds 10
}

if ($retryCount -eq $maxRetries) {
    Write-Log "❌ Application failed to become healthy" $Red
    Write-Log "Rolling back deployment..." $Red
    docker-compose down
    exit 1
}

# Post-deployment verification
Write-Log "🔍 Running post-deployment verification..." $Blue

$endpoints = @("/health", "/api/agents/status")

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000$endpoint" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ $endpoint is responding" $Green
        }
        else {
            Write-Log "❌ $endpoint returned status $($response.StatusCode)" $Red
        }
    }
    catch {
        Write-Log "❌ $endpoint is not responding: $($_.Exception.Message)" $Red
    }
}

Write-Log "🎉 ButterflyBlue Creations launched successfully!" $Green
Write-Log "Application is running at: http://localhost:8000" $Green

# Display final status
Write-Host ""
Write-Host "==================================================" -ForegroundColor $Green
Write-Host "🦋 LAUNCH COMPLETE" -ForegroundColor $Green
Write-Host "==================================================" -ForegroundColor $Green
Write-Host "Environment: $Environment"
Write-Host "Version: $Version"
Write-Host "Status: LIVE"
Write-Host "Health Check: http://localhost:8000/health"
Write-Host "API Documentation: http://localhost:8000/docs"
Write-Host "==================================================" -ForegroundColor $Green