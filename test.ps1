# ButterflyBlue Creations - Comprehensive Test Script
Write-Host "🧪 Testing ButterflyBlue Creations System..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"
$testResults = @()

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Body = $null,
        [int]$ExpectedStatus = 200
    )
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            UseBasicParsing = $true
            TimeoutSec = 10
        }
        
        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json)
            $params.ContentType = "application/json"
        }
        
        $response = Invoke-WebRequest @params
        
        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-Host "✅ $Name" -ForegroundColor Green
            return @{Name=$Name; Status="PASS"; Details="Status: $($response.StatusCode)"}
        } else {
            Write-Host "❌ $Name - Unexpected status: $($response.StatusCode)" -ForegroundColor Red
            return @{Name=$Name; Status="FAIL"; Details="Expected: $ExpectedStatus, Got: $($response.StatusCode)"}
        }
    }
    catch {
        Write-Host "❌ $Name - Error: $($_.Exception.Message)" -ForegroundColor Red
        return @{Name=$Name; Status="FAIL"; Details=$_.Exception.Message}
    }
}

# Test 1: Health Check
Write-Host "`n🔍 Testing Core Services..." -ForegroundColor Blue
$testResults += Test-Endpoint -Name "Health Check" -Url "$baseUrl/health"

# Test 2: API Documentation
$testResults += Test-Endpoint -Name "API Documentation" -Url "$baseUrl/docs"

# Test 3: Agent Status
$testResults += Test-Endpoint -Name "Agent Status" -Url "$baseUrl/api/agents/status"

# Test 4: Boss Agent
Write-Host "`n👑 Testing Boss Agent..." -ForegroundColor Blue
$bossTask = @{
    task_type = "coordinate"
    description = "Test coordination task"
    priority = "high"
}
$testResults += Test-Endpoint -Name "Boss Agent Task" -Url "$baseUrl/api/agents/boss/task" -Method "POST" -Body $bossTask

# Test 5: Marketing Agent
Write-Host "`n📈 Testing Marketing Agent..." -ForegroundColor Blue
$marketingCampaign = @{
    campaign_type = "social_media"
    target_audience = "small businesses"
    budget = 1000
    platforms = @("facebook", "instagram")
}
$testResults += Test-Endpoint -Name "Marketing Campaign" -Url "$baseUrl/api/agents/marketing/campaign" -Method "POST" -Body $marketingCampaign

# Test 6: Finance Agent
Write-Host "`n💰 Testing Finance Agent..." -ForegroundColor Blue
$paymentData = @{
    amount = 100.00
    currency = "ZAR"
    gateway = "paystack"
    customer_email = "test@example.com"
}
$testResults += Test-Endpoint -Name "Payment Processing" -Url "$baseUrl/api/agents/finance/payment" -Method "POST" -Body $paymentData

# Test 7: Customer Service Agent
Write-Host "`n🎧 Testing Customer Service Agent..." -ForegroundColor Blue
$supportTicket = @{
    subject = "Test Support Ticket"
    description = "This is a test support ticket"
    priority = "medium"
    channel = "email"
}
$testResults += Test-Endpoint -Name "Support Ticket" -Url "$baseUrl/api/agents/customer-service/ticket" -Method "POST" -Body $supportTicket

# Test 8: Design Agent
Write-Host "`n🎨 Testing Design Agent..." -ForegroundColor Blue
$designRequest = @{
    design_type = "landing_page"
    style = "modern"
    brand_colors = @("#007bff", "#28a745")
    content = "ButterflyBlue Creations"
}
$testResults += Test-Endpoint -Name "Design Generation" -Url "$baseUrl/api/agents/design/generate" -Method "POST" -Body $designRequest

# Test 9: Engineering Agent
Write-Host "`n⚙️ Testing Engineering Agent..." -ForegroundColor Blue
$codeProject = @{
    project_type = "api"
    framework = "fastapi"
    features = @("authentication", "database", "testing")
    name = "test-project"
}
$testResults += Test-Endpoint -Name "Code Generation" -Url "$baseUrl/api/agents/engineering/generate" -Method "POST" -Body $codeProject

# Test 10: Database Connectivity
Write-Host "`n🗄️ Testing Database..." -ForegroundColor Blue
$testResults += Test-Endpoint -Name "Database Health" -Url "$baseUrl/api/health/database"

# Test 11: Redis Connectivity
Write-Host "`n🔄 Testing Cache..." -ForegroundColor Blue
$testResults += Test-Endpoint -Name "Cache Health" -Url "$baseUrl/api/health/cache"

# Test 12: MQTT Connectivity
Write-Host "`n📡 Testing Message Queue..." -ForegroundColor Blue
$testResults += Test-Endpoint -Name "MQTT Health" -Url "$baseUrl/api/health/mqtt"

# Performance Test
Write-Host "`n⚡ Running Performance Test..." -ForegroundColor Blue
$startTime = Get-Date
try {
    1..10 | ForEach-Object {
        Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing -TimeoutSec 5 | Out-Null
    }
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalMilliseconds
    $avgResponse = $duration / 10
    
    if ($avgResponse -lt 1000) {
        Write-Host "✅ Performance Test - Avg Response: $([math]::Round($avgResponse, 2))ms" -ForegroundColor Green
        $testResults += @{Name="Performance Test"; Status="PASS"; Details="Avg Response: $([math]::Round($avgResponse, 2))ms"}
    } else {
        Write-Host "⚠️ Performance Test - Slow Response: $([math]::Round($avgResponse, 2))ms" -ForegroundColor Yellow
        $testResults += @{Name="Performance Test"; Status="WARN"; Details="Avg Response: $([math]::Round($avgResponse, 2))ms"}
    }
}
catch {
    Write-Host "❌ Performance Test Failed" -ForegroundColor Red
    $testResults += @{Name="Performance Test"; Status="FAIL"; Details=$_.Exception.Message}
}

# Generate Test Report
Write-Host "`n📊 Test Results Summary" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

$passCount = ($testResults | Where-Object {$_.Status -eq "PASS"}).Count
$failCount = ($testResults | Where-Object {$_.Status -eq "FAIL"}).Count
$warnCount = ($testResults | Where-Object {$_.Status -eq "WARN"}).Count
$totalTests = $testResults.Count

Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: $passCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor Red
Write-Host "Warnings: $warnCount" -ForegroundColor Yellow

if ($failCount -eq 0) {
    Write-Host "`n🎉 All tests passed! ButterflyBlue is ready for action!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ Some tests failed. Please check the logs for details." -ForegroundColor Yellow
    Write-Host "Failed tests:" -ForegroundColor Red
    $testResults | Where-Object {$_.Status -eq "FAIL"} | ForEach-Object {
        Write-Host "  - $($_.Name): $($_.Details)" -ForegroundColor Red
    }
}

# Save detailed report
$reportPath = "test-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
$testResults | ConvertTo-Json -Depth 3 | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "`n📄 Detailed report saved to: $reportPath" -ForegroundColor Cyan