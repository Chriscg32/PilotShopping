# Quick Start Script for ButterflyBlue Creations
Write-Host "🦋 Starting ButterflyBlue Creations..." -ForegroundColor Cyan

# Set required environment variables
$env:JWT_SECRET_KEY = "your-super-secret-jwt-key-change-this-in-production"
$env:PAYSTACK_SECRET_KEY = "sk_test_your_paystack_secret_key"
$env:PAYPAL_CLIENT_ID = "your_paypal_client_id"
$env:PAYPAL_CLIENT_SECRET = "your_paypal_client_secret"

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Start the application
Write-Host "🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d --build

# Wait for startup
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Check health
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ ButterflyBlue is running successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 Access your application:" -ForegroundColor Cyan
        Write-Host "   Main App: http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
        Write-Host "   Health Check: http://localhost:8000/health" -ForegroundColor White
    }
}
catch {
    Write-Host "⚠️ Application may still be starting up..." -ForegroundColor Yellow
    Write-Host "Please wait a moment and check http://localhost:8000/health" -ForegroundColor Yellow
}