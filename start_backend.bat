@echo off
echo ========================================
echo Quantum State Visualizer - Backend
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "env" (
    echo Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo Failed to create virtual environment. Trying with python3...
        python3 -m venv env
        if errorlevel 1 (
            echo Failed to create virtual environment. Please check Python installation.
            pause
            exit /b 1
        )
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Upgrade pip and setuptools
echo Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

REM Install requirements
echo Installing backend dependencies...
pip install -r backend\requirements.txt

REM Test backend
echo Testing backend...
python backend\test_backend.py

REM Start backend server
echo.
echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo.
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
