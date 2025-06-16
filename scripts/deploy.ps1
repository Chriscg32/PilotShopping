# Windows PowerShell deployment script
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("development", "staging", "production")]
    [string]$Environment
)

Write-Host "🚀 Deploying Landing Copy Generator to $Environment environment..." -ForegroundColor Green

# Set environment variables based on target
switch ($Environment) {
    "development" {
        $env:ENVIRONMENT = "development"
        $ComposeFile = "docker-compose.dev.yml"
    }
    "staging" {
        $env:ENVIRONMENT = "staging" 
        $ComposeFile = "docker-compose.yml"
    }
    "production" {
        $env:ENVIRONMENT = "production"
        $ComposeFile = "docker-compose.yml"
    }
}

Write-Host "📋 Environment: $Environment" -ForegroundColor Yellow

# Check if Docker is available
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is available" -ForegroundColor Green
    
    # Check if docker-compose file exists
    if (Test-Path $ComposeFile) {
        Write-Host "🔨 Building and starting containers..." -ForegroundColor Yellow
        docker-compose -f $ComposeFile up --build -d
    } else {
        Write-Host "⚠️ Docker compose file not found. Running locally..." -ForegroundColor Yellow
        python main.py
    }
} catch {
    Write-Host "⚠️ Docker not available. Running locally..." -ForegroundColor Yellow
    
    # Check if virtual environment exists
    if (-not (Test-Path "venv")) {
        Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
    }
    
    # Activate virtual environment
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    
    # Install dependencies if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt
    }
    
    # Run the application
    Write-Host "🚀 Starting application..." -ForegroundColor Green
    python main.py
}

Write-Host "🎉 Deployment complete!" -ForegroundColor Green
Write-Host "📊 API available at: http://localhost:8000" -ForegroundColor Cyan