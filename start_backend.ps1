# Quantum State Visualizer - Backend Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Quantum State Visualizer - Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "env")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    
    # Try different Python commands
    $pythonCommands = @("python", "python3", "py")
    $venvCreated = $false
    
    foreach ($cmd in $pythonCommands) {
        try {
            & $cmd -m venv env
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Virtual environment created successfully with $cmd" -ForegroundColor Green
                $venvCreated = $true
                break
            }
        } catch {
            Write-Host "Failed to create virtual environment with $cmd" -ForegroundColor Red
        }
    }
    
    if (-not $venvCreated) {
        Write-Host "Failed to create virtual environment. Please check Python installation." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & "env\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        throw "Activation failed"
    }
} catch {
    Write-Host "Failed to activate virtual environment." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Upgrade pip and setuptools
Write-Host "Upgrading pip and setuptools..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Install requirements
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
pip install -r backend\requirements.txt

# Test backend
Write-Host "Testing backend..." -ForegroundColor Yellow
python backend\test_backend.py

# Start backend server
Write-Host ""
Write-Host "Starting backend server..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs will be available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
