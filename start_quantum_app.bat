@echo off
echo 🚀 Starting Quantum State Visualizer...
echo.

echo 📡 Starting Backend (Port 8005)...
start "Quantum Backend" cmd /k "cd backend && python main_minimal.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo 🌐 Starting Frontend (Port 3000)...
start "Quantum Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Quantum State Visualizer is starting up!
echo 📍 Backend: http://localhost:8005
echo 📍 Frontend: http://localhost:3000
echo.
echo 🎯 Use the working minimal backend for now
echo 🔧 The main backend has some import issues being resolved
echo.
pause
