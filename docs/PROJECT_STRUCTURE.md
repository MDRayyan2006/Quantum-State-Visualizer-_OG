# 🚀 Quantum State Visualizer - Project Structure

## 📁 Root Directory
```
LastHope/
├── README.md                    # Main project documentation
├── PROJECT_STRUCTURE.md         # This file - project structure overview
├── docker-compose.yml          # Docker services configuration
├── start.bat                   # Windows startup script
├── start.sh                    # Unix/Linux startup script
├── backend/                    # Python FastAPI backend
└── frontend/                   # React TypeScript frontend
```

## 🔧 Backend Structure (`backend/`)
```
backend/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend container configuration
├── api/                        # API route modules
│   ├── __init__.py
│   ├── quantum.py             # Core quantum simulation endpoints
│   ├── algorithms.py          # Quantum algorithm implementations
│   └── export.py              # Export and reporting endpoints
├── dash_app.py                 # Plotly Dash analytics dashboard
└── static/                     # Static files served by FastAPI
```

### 🔬 Core API Endpoints
- **`POST /api/simulate`** - Run quantum circuit simulation
- **`POST /api/rdm`** - Compute reduced density matrices
- **`POST /api/bloch`** - Get Bloch sphere parameters
- **`POST /api/entanglement`** - Analyze entanglement between qubits
- **`POST /api/algorithms/{vqe|qaoa|grover|qft|teleport}`** - Run quantum algorithms
- **`POST /api/export/generate`** - Export results in various formats
- **`GET /dash`** - Advanced analytics dashboard

### 🧮 Quantum Algorithms Implemented
- **VQE** (Variational Quantum Eigensolver) - H₂ molecule
- **QAOA** (Quantum Approximate Optimization Algorithm) - MaxCut problem
- **Grover's Search** - Quantum search algorithm
- **QFT** (Quantum Fourier Transform) - Quantum signal processing
- **Quantum Teleportation** - Quantum communication protocol

## 🎨 Frontend Structure (`frontend/`)
```
frontend/
├── package.json                # Node.js dependencies and scripts
├── vite.config.ts             # Vite build configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── index.html                  # HTML entry point
├── src/                        # React source code
│   ├── main.tsx               # Application entry point
│   ├── App.tsx                # Main App component with routing
│   ├── index.css              # Global styles and Tailwind imports
│   ├── contexts/              # React context providers
│   │   └── QuantumContext.tsx # Global quantum state management
│   ├── components/            # Reusable UI components
│   │   └── Navbar.tsx         # Navigation component
│   └── pages/                 # Application pages
│       ├── Dashboard.tsx      # Main dashboard page
│       ├── CircuitEditor.tsx  # Quantum circuit editor (TODO)
│       ├── Algorithms.tsx     # Algorithm library (TODO)
│       └── Analytics.tsx      # Analytics dashboard (TODO)
└── Dockerfile                  # Frontend container configuration
```

### 🎯 Frontend Features
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Dark Theme** - Quantum-inspired dark color scheme
- **Animations** - Smooth transitions with Framer Motion
- **TypeScript** - Full type safety and IntelliSense
- **Component Architecture** - Modular, reusable components

## 🐳 Docker Configuration
- **`docker-compose.yml`** - Orchestrates both services
- **`backend/Dockerfile`** - Python 3.9 slim container
- **`frontend/Dockerfile`** - Node.js 18 Alpine container
- **Network** - Isolated `quantum-network` for service communication

## 🚀 Quick Start Options

### Option 1: Automated Scripts
- **Windows**: Run `start.bat`
- **Unix/Linux**: Run `./start.sh` (make executable with `chmod +x start.sh`)

### Option 2: Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Option 3: Docker
```bash
docker-compose up --build
```

## 🌐 Service URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Analytics Dashboard**: http://localhost:8000/dash
- **Health Check**: http://localhost:8000/health

## 📊 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Qiskit** - Quantum computing framework
- **QuTiP** - Quantum toolbox for Python
- **NumPy/SciPy** - Scientific computing
- **Plotly/Dash** - Interactive visualizations
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Router** - Client-side routing
- **Plotly.js** - Interactive plotting

### Development Tools
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Docker** - Containerization
- **Git** - Version control

## 🔍 Key Features

### 🧮 Quantum Simulation
- **Circuit Parsing** - OpenQASM 2.0/3.0 support
- **State Vector Simulation** - Exact quantum state computation
- **Density Matrix** - Mixed state representation
- **Noise Models** - Realistic quantum error simulation
- **Multiple Backends** - Aer simulator, statevector, etc.

### 📊 Visualization
- **Bloch Spheres** - 3D qubit state visualization
- **Density Matrix Heatmaps** - State representation
- **Entanglement Analysis** - Bipartite entropy, concurrence
- **Algorithm Trajectories** - Convergence plots
- **Real-time Metrics** - Live performance monitoring

### 📈 Analytics
- **Parameter Sweeps** - Systematic exploration
- **Noise Impact Analysis** - Error sensitivity studies
- **Performance Metrics** - Execution time, success rates
- **Export Capabilities** - PDF reports, PNG images, JSON data

## 🎯 Development Roadmap

### Phase 1: Core Infrastructure ✅
- [x] Backend API structure
- [x] Basic quantum simulation
- [x] Frontend routing and components
- [x] Docker configuration

### Phase 2: Circuit Editor 🚧
- [ ] Drag-and-drop circuit builder
- [ ] OpenQASM editor with syntax highlighting
- [ ] Circuit validation and optimization
- [ ] Gate library and templates

### Phase 3: Advanced Visualizations 🚧
- [ ] Interactive Bloch spheres
- [ ] 3D circuit diagrams
- [ ] Real-time state evolution
- [ ] Custom plotting options

### Phase 4: Algorithm Library 🚧
- [ ] VQE implementation with real molecules
- [ ] QAOA for various optimization problems
- [ ] Grover's algorithm with custom oracles
- [ ] Quantum machine learning algorithms

### Phase 5: Production Features 🚧
- [ ] User authentication and accounts
- [ ] Cloud deployment options
- [ ] Performance optimization
- [ ] Comprehensive testing suite

## 🤝 Contributing
This is a hackathon project! Contributions are welcome:
- Bug reports and feature requests
- Code improvements and optimizations
- Documentation and examples
- Testing and validation

## 📄 License
MIT License - Open source for the quantum community!

---

**🚀 Ready to explore quantum computing? Start with the Dashboard and build your first quantum circuit!**
