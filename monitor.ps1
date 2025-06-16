# ButterflyBlue Creations - System Monitor
param(
    [int]$IntervalSeconds = 30,
    [switch]$Continuous = $false
)

function Get-ServiceStatus {
    Write-Host "🔍 ButterflyBlue System Status - $(Get-Date)" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # Docker containers status
    Write-Host "`n🐳 Container Status:" -ForegroundColor Blue
    try {
        $containers = docker-compose ps --format json | ConvertFrom-Json
        foreach ($container in $containers) {
            $status = if ($container.State -eq "running") { "✅" } else { "❌" }
            Write-Host "  $status $($container.Service): $($container.State)" -ForegroundColor $(if ($container.State -eq "running") { "Green" } else { "Red" })
        }
    }
    catch {
        Write-Host "  ❌ Unable to get container status" -ForegroundColor Red
    }
    
    # Service health checks
    Write-Host "`n🏥 Health Checks:" -ForegroundColor Blue
    
    $healthChecks = @(
        @{Name="Application"; Url="http://localhost:8000/health"},
        @{Name="Database"; Url="http://localhost:8000/api/health/database"},
        @{Name="Cache"; Url="http://localhost:8000/api/health/cache"},
        @{Name="MQTT"; Url="http://localhost:8000/api/health/mqtt"}
    )
    
    foreach ($check in $healthChecks) {
        try {
            $response = Invoke-WebRequest -Uri $check.Url -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "  ✅ $($check.Name): Healthy" -ForegroundColor Green
            } else {
                Write-Host "  ❌ $($check.Name): Unhealthy (Status: $($response.StatusCode))" -ForegroundColor Red
            }
        }
        catch {
            Write-Host "  ❌ $($check.Name): Unreachable" -ForegroundColor Red
        }
    }
    
    # Resource usage
    Write-Host "`n📊 Resource Usage:" -ForegroundColor Blue
    try {
        $stats = docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" | Select-Object -Skip 1
        foreach ($line in $stats) {
            if ($line.Trim()) {
                Write-Host "  📈 $line" -ForegroundColor White
            }
        }
    }
    catch {
        Write-Host "  ❌ Unable to get resource stats" -ForegroundColor Red
    }
    
    # Agent status
    Write-Host "`n🤖 Agent Status:" -ForegroundColor Blue
    try {
        $agentResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/agents/status" -TimeoutSec 5
        foreach ($agent in $agentResponse.agents) {
            $status = if ($agent.status -eq "online") { "✅" } else { "❌" }
            Write-Host "  $status $($agent.name): $($agent.status) (Tasks: $($agent.tasks_completed))" -ForegroundColor $(if ($agent.status -eq "online") { "Green" } else { "Red" })
        }
    }
    catch {
        Write-Host "  ❌ Unable to get agent status" -ForegroundColor Red
    }
    
    Write-Host "`n" -ForegroundColor White
}

# Run monitoring
if ($Continuous) {
    Write-Host "🔄 Starting continuous monitoring (Ctrl+C to stop)..." -ForegroundColor Yellow
    Write-Host "Refresh interval: $IntervalSeconds seconds" -ForegroundColor Yellow
    
    while ($true) {
        Clear-Host
        Get-ServiceStatus
        Start-Sleep -Seconds $IntervalSeconds
    }
} else {
    Get-ServiceStatus
}