# Quantum State Visualizer - Backend

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (3.13 recommended)
- pip (latest version)
- Virtual environment support

### Option 1: Automated Setup (Windows)
```cmd
# Run the batch file
start_backend.bat
```

### Option 2: Automated Setup (PowerShell)
```powershell
# Run the PowerShell script
.\start_backend.ps1
```

### Option 3: Manual Setup
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# Unix/Mac:
source env/bin/activate

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Test backend
python test_backend.py

# Start server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📦 Dependencies

### Core Framework
- **FastAPI 0.120.0** - Modern, fast web framework
- **Uvicorn 0.32.1** - ASGI server

### Quantum Computing
- **Qiskit 1.1.2** - Quantum computing framework
- **Qiskit Aer 0.14.1** - Quantum simulators
- **QuTiP 5.2.0** - Quantum toolbox

### Scientific Computing
- **NumPy 1.26.4** - Numerical computing
- **SciPy 1.13.0** - Scientific algorithms

### Visualization
- **Plotly 5.21.0** - Interactive plots
- **Dash 2.18.0** - Web applications
- **Matplotlib 3.9.1** - Plotting library
- **Seaborn 0.13.2** - Statistical visualization

### Data Processing
- **Pandas 2.2.2** - Data manipulation
- **NetworkX 3.3** - Graph algorithms

### Utilities
- **Pydantic 2.10.1** - Data validation
- **Jinja2 3.1.3** - Template engine
- **ReportLab 4.1.0** - PDF generation
- **Pillow 10.5.0** - Image processing

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Version Issues
```bash
# Check Python version
python --version

# Should be 3.8+ for best compatibility
# Python 3.13 is fully supported
```

#### 2. Virtual Environment Issues
```bash
# Remove existing environment
rm -rf env/  # Unix/Mac
rmdir /s env  # Windows

# Recreate environment
python -m venv env
```

#### 3. Package Installation Issues
```bash
# Clear pip cache
pip cache purge

# Install with verbose output
pip install -r requirements.txt -v

# Try minimal requirements
pip install -r requirements-minimal.txt
```

#### 4. Qiskit Compatibility Issues
```bash
# Qiskit 1.x requires Python 3.8+
# If using older Python, downgrade Qiskit:
pip install "qiskit<1.0"
```

#### 5. NumPy/SciPy Compilation Issues
```bash
# Install pre-compiled wheels
pip install --only-binary=all numpy scipy

# Or use conda for better binary support
conda install numpy scipy
```

### Testing Backend

Run the test script to verify everything works:
```bash
python test_backend.py
```

Expected output:
```
🧪 Testing Quantum State Visualizer Backend

Testing imports...
✅ FastAPI 0.120.0
✅ Uvicorn 0.32.1
✅ Qiskit 1.1.2
✅ Qiskit Aer
✅ QuTiP 5.2.0
✅ NumPy 1.26.4
✅ SciPy 1.13.0
✅ Plotly 5.21.0
✅ Dash 2.18.0
✅ Pandas 2.2.2
✅ Pydantic 2.10.1

🎉 All imports successful! Backend should work correctly.

Testing basic quantum functionality...
✅ Qiskit circuit creation
✅ QuTiP basic operations
✅ NumPy operations
🎉 Basic functionality tests passed!

🚀 Backend is ready to run!
```

## 🌐 API Endpoints

Once running, the backend provides:

- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Dash Analytics**: http://localhost:8000/dash
- **Health Check**: http://localhost:8000/health

## 🔄 Development

### Hot Reload
The server runs with `--reload` flag for development:
- Code changes automatically restart the server
- No need to manually restart

### Logging
Check console output for:
- Startup messages
- API requests
- Error details

### Environment Variables
Create `.env` file for configuration:
```env
DEBUG=true
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [QuTiP Documentation](https://qutip.org/docs/latest/)
- [Python 3.13 Features](https://docs.python.org/3.13/whatsnew/3.13.html)
