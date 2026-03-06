$body = @{
    message = "What is superposition?"
    context = "quantum_education"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method Post -ContentType "application/json" -Body $body
    Write-Host "✅ Chat API Working!"
    Write-Host "Response: $($response.response)"
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)"
}