# Quick Database Fix Script
Write-Host "🔧 Fixing ButterflyBlue Database..." -ForegroundColor Cyan

# Stop services
Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
docker-compose down

# Remove old volumes to start fresh
Write-Host "🗑️ Cleaning old data..." -ForegroundColor Yellow
docker volume rm butterflyblue_postgres_data -f 2>$null

# Ensure init directory exists with proper SQL
Write-Host "📁 Setting up database initialization..." -ForegroundColor Yellow
if (!(Test-Path "init")) {
    New-Item -ItemType Directory -Path "init" -Force
}

# Create the database initialization script
$initSQL = @"
-- Create the butterflyblue database and user
CREATE DATABASE butterflyblue;
CREATE USER butterflyblue_user WITH PASSWORD 'butterflyblue123';
GRANT ALL PRIVILEGES ON DATABASE butterflyblue TO butterflyblue_user;

-- Connect to the database
\c butterflyblue;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'offline',
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tasks_completed INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default agents
INSERT INTO agents (name, type, status) VALUES
    ('boss', 'coordinator', 'online'),
    ('marketing', 'marketing', 'online'),
    ('finance', 'finance', 'online'),
    ('customer-service', 'support', 'online'),
    ('engineering', 'development', 'online'),
    ('design', 'creative', 'online');

-- Create a demo user
INSERT INTO users (email, username, password_hash) VALUES
    ('demo@butterflyblue.co.za', 'demo', crypt('demo123', gen_salt('bf')));

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO butterflyblue_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO butterflyblue_user;
"@

$initSQL | Out-File -FilePath "init/01-init-db.sql" -Encoding UTF8
Write-Host "✅ Database initialization script created" -ForegroundColor Green

# Start services
Write-Host "🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d

# Wait for database to initialize
Write-Host "⏳ Waiting for database to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Test database connection
Write-Host "🔍 Testing database connection..." -ForegroundColor Blue
$maxRetries = 10
$retryCount = 0

while ($retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Database is working!" -ForegroundColor Green
            break
        }
    }
    catch {
        $retryCount++
        Write-Host "⏳ Attempt $retryCount/$maxRetries - Still waiting..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
    }
}

if ($retryCount -eq $maxRetries) {
    Write-Host "❌ Database setup may have failed. Check logs with: docker-compose logs postgres" -ForegroundColor Red
} else {
    Write-Host "🎉 Database fixed successfully!" -ForegroundColor Green
    Write-Host "🌐 Application is ready at: http://localhost:8000" -ForegroundColor Cyan
}
