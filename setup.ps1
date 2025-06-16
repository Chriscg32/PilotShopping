# ButterflyBlue Creations - Setup Script
Write-Host "🦋 Setting up ButterflyBlue Creations..." -ForegroundColor Cyan

# Create necessary directories
$directories = @("init", "config", "ssl", "data", "logs")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Create mosquitto config
$mosquittoConfig = @"
listener 1883
allow_anonymous true
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
"@

$mosquittoConfig | Out-File -FilePath "config/mosquitto.conf" -Encoding UTF8
Write-Host "✅ Created MQTT configuration" -ForegroundColor Green

# Create nginx config
$nginxConfig = @"
events {
    worker_connections 1024;
}

http {
    upstream butterflyblue_app {
        server app:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://butterflyblue_app;
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
            proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto `$scheme;
        }

        location /health {
            proxy_pass http://butterflyblue_app/health;
            access_log off;
        }
    }
}
"@

$nginxConfig | Out-File -FilePath "config/nginx.conf" -Encoding UTF8
Write-Host "✅ Created Nginx configuration" -ForegroundColor Green

# Set environment variables
$env:JWT_SECRET_KEY = "butterflyblue-super-secret-jwt-key-2024"
$env:PAYSTACK_SECRET_KEY = "sk_test_your_paystack_secret_key"
$env:PAYPAL_CLIENT_ID = "your_paypal_client_id"
$env:PAYPAL_CLIENT_SECRET = "your_paypal_client_secret"

Write-Host "✅ Environment variables set" -ForegroundColor Green

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down -v

# Build and start services
Write-Host "🚀 Building and starting services..." -ForegroundColor Cyan
docker-compose up -d --build

# Wait for services to be ready
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Cyan

$services = @(
    @{Name="PostgreSQL"; Port=5432; Host="localhost"},
    @{Name="Redis"; Port=6379; Host="localhost"},
    @{Name="MQTT"; Port=1883; Host="localhost"},
    @{Name="Application"; Port=8000; Host="localhost"; Path="/health"},
    @{Name="Grafana"; Port=3000; Host="localhost"}
)

foreach ($service in $services) {
    try {
        if ($service.Path) {
            $response = Invoke-WebRequest -Uri "http://$($service.Host):$($service.Port)$($service.Path)" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ $($service.Name) is healthy" -ForegroundColor Green
            }
        } else {
            $connection = Test-NetConnection -ComputerName $service.Host -Port $service.Port -WarningAction SilentlyContinue
            if ($connection.TcpTestSucceeded) {
                Write-Host "✅ $($service.Name) is running" -ForegroundColor Green
            } else {
                Write-Host "❌ $($service.Name) is not responding" -ForegroundColor Red
            }
        }
    }
    catch {
        Write-Host "❌ $($service.Name) health check failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 ButterflyBlue Creations setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your services:" -ForegroundColor Cyan
Write-Host "   Main Application: http://localhost:8000" -ForegroundColor White
Write-Host "   API Documentation: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host "   Grafana Dashboard: http://localhost:3000 (admin/admin123)" -ForegroundColor White
Write-Host "   Database: localhost:5432 (butterflyblue_user/butterflyblue123)" -ForegroundColor White
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit http://localhost:8000 to access the application"
Write-Host "2. Check http://localhost:8000/docs for API documentation"
Write-Host "3. Monitor services at http://localhost:3000 (Grafana)"
Write-Host "4. Run './test.ps1' to verify all functionality"
Write-Host ""
Write-Host "🔧 Troubleshooting:" -ForegroundColor Yellow
Write-Host "- View logs: docker-compose logs -f [service-name]"
Write-Host "- Restart services: docker-compose restart"
Write-Host "- Reset everything: docker-compose down -v && ./setup.ps1"