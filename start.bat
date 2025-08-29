@echo off
echo 🚀 Starting Quantum State Visualizer...
echo.

echo 📦 Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo 📦 Installing Node.js dependencies...
cd ../frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo 🎯 Starting services...
echo.

echo 🔧 Starting Backend (FastAPI)...
start "Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🎨 Starting Frontend (React)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Quantum State Visualizer is starting up!
echo.
echo 🌐 Backend API: http://localhost:8000
echo 🎨 Frontend: http://localhost:3000
echo 📊 Analytics: http://localhost:8000/dash
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to open the application...
pause > nul

start http://localhost:3000
start http://localhost:8000/docs

echo.
echo 🎉 Enjoy exploring quantum computing!
pause
