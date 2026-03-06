@echo off
echo Starting Quantum State Visualizer...
echo.

echo Starting Backend Server...
start cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Quantum State Visualizer Started!
echo ========================================
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Dash Analytics: http://localhost:8000/dash
echo ========================================
echo.
echo Press any key to exit...
pause > nul