@echo off
echo 🚀 Starting Quantum State Visualizer Services...
echo.

echo 📦 Starting Backend Server...
cd backend
start "Backend Server" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8002"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo 🌐 Starting Frontend Server...
cd ..\frontend
start "Frontend Server" cmd /k "npm run dev"

echo ⏳ Waiting for frontend to start...
timeout /t 5 /nobreak > nul

echo.
echo ✅ Services are starting up!
echo.
echo 📊 Backend API: http://localhost:8002
echo 🌐 Frontend App: http://localhost:3000
echo 📚 API Docs: http://localhost:8002/docs
echo.
echo 🎯 The Quantum State Visualizer is now running!
echo.
pause
