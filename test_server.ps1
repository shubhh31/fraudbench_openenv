# Test FastAPI server on localhost:8000

# 1. GET /health
Write-Host "Testing GET /health..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
    Write-Host "Response: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# 2. POST /reset
Write-Host "`nTesting POST /reset..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/reset" -Method POST
    Write-Host "Response: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# 3. POST /step with body
Write-Host "`nTesting POST /step..."
$body = '{"decision":"approve","reason":"test"}'
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/step" -Method POST -Body $body -ContentType "application/json"
    Write-Host "Response: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}