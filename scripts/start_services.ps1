# Quantum State Visualizer Startup Script
Write-Host "🚀 Starting Quantum State Visualizer Services..." -ForegroundColor Green
Write-Host ""

# Start Backend Server
Write-Host "📦 Starting Backend Server..." -ForegroundColor Cyan
Set-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn main:app --host 0.0.0.0 --port 8002"

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host "🌐 Starting Frontend Server..." -ForegroundColor Cyan
Set-Location ..\frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"

# Wait for frontend to start
Write-Host "⏳ Waiting for frontend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✅ Services are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Backend API: http://localhost:8002" -ForegroundColor White
Write-Host "🌐 Frontend App: http://localhost:3000" -ForegroundColor White
Write-Host "📚 API Docs: http://localhost:8002/docs" -ForegroundColor White
Write-Host ""
Write-Host "🎯 The Quantum State Visualizer is now running!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to continue..."
