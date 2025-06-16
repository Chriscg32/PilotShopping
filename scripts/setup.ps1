# ButterflyBlue Creations - PowerShell Setup Script
Write-Host "🦋 ButterflyBlue Creations - Setup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Create directory structure
$directories = @("logs", "data", "temp", "backups", "tests/unit", "tests/integration", "tests/e2e", "app/agents", "app/core", "app/api", "app/models", "app/services")

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Copy environment file
if (!(Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file from template" -ForegroundColor Green
    } else {
        # Create basic .env file
        @"
# ButterflyBlue Creations Configuration
DATABASE_URL=sqlite:///./butterflyblue.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
HUGGINGFACE_API_KEY=your-huggingface-key
PAYSTACK_SECRET_KEY=your-paystack-key
PAYPAL_CLIENT_ID=your-paypal-client-id
ENVIRONMENT=development
DEBUG=true
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Created basic .env file" -ForegroundColor Green
    }
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host "Run 'python main.py' to start the application." -ForegroundColor Cyan