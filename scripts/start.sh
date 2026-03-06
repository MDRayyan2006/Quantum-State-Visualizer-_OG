#!/bin/bash

echo "🚀 Starting Quantum State Visualizer..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "📦 Installing Node.js dependencies..."
cd ../frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

echo
echo "🎯 Starting services..."
echo

echo "🔧 Starting Backend (FastAPI)..."
cd ../backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "⏳ Waiting for backend to start..."
sleep 5

echo "🎨 Starting Frontend (React)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo
echo "✅ Quantum State Visualizer is starting up!"
echo
echo "🌐 Backend API: http://localhost:8000"
echo "🎨 Frontend: http://localhost:3000"
echo "📊 Analytics: http://localhost:8000/dash"
echo "📚 API Docs: http://localhost:8000/docs"
echo

# Function to cleanup on exit
cleanup() {
    echo
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo "Press Ctrl+C to stop all services"
echo

# Wait for user to stop
wait
