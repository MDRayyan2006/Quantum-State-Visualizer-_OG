from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from contextlib import asynccontextmanager
import os

from api.quantum import router as quantum_router
from api.algorithms import router as algorithms_router
from api.export import router as export_router
from api.chat import router as chat_router
from dash_app import create_dash_app

# Global state for storing simulation results
simulation_results = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Quantum State Visualizer...")
    print("📊 Initializing Dash Analytics Dashboard...")
    yield
    # Shutdown
    print("🛑 Shutting down Quantum State Visualizer...")

app = FastAPI(
    title="Quantum State Visualizer (QSV)",
    description="Visualize quantum states, compute reduced density matrices, and explore quantum algorithms",
    version="1.0.0",
    lifespan=lifespan
)

# Create and mount Dash app
try:
    dash_app = create_dash_app()
    app.mount("/dash", WSGIMiddleware(dash_app.server))
    print("✅ Dash app mounted successfully at /dash")
except Exception as e:
    print(f"❌ Failed to mount Dash app: {e}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quantum_router, prefix="/api/quantum", tags=["quantum"])
app.include_router(algorithms_router, prefix="/api/algorithms", tags=["algorithms"])
app.include_router(export_router, prefix="/api/export", tags=["export"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quantum State Visualizer API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #0f0f23; color: #fff; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #00ff88; text-align: center; }
            .endpoint { background: #1a1a2e; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 4px solid #00ff88; }
            .method { color: #00ff88; font-weight: bold; }
            .url { color: #ff6b6b; font-family: monospace; }
            .description { color: #ddd; }
            .docs-link { text-align: center; margin: 30px 0; }
            .docs-link a { background: #00ff88; color: #000; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Quantum State Visualizer API</h1>
            <p style="text-align: center; color: #00ff88; font-size: 18px;">Advanced quantum computing visualization and analysis platform</p>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/health</div>
                <div class="description">Check API health status</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/quantum/simulate</div>
                <div class="description">Run quantum circuit simulation and get statevector/density matrix</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/quantum/rdm</div>
                <div class="description">Compute reduced density matrices for specified qubits</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/quantum/bloch</div>
                <div class="description">Compute Bloch sphere parameters for qubits</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/quantum/entanglement</div>
                <div class="description">Analyze entanglement between qubit pairs</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/api/quantum/simulations</div>
                <div class="description">List all stored simulation results</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/algorithms/vqe</div>
                <div class="description">Run Variational Quantum Eigensolver (VQE)</div>
            </div>

            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/algorithms/grover</div>
                <div class="description">Run Grover's search algorithm</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/algorithms/qft</div>
                <div class="description">Run Quantum Fourier Transform (QFT)</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/algorithms/teleport</div>
                <div class="description">Run quantum teleportation protocol</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/chat</div>
                <div class="description">Educational quantum computing chatbot powered by Mistral AI</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/export/report</div>
                <div class="description">Generate comprehensive PDF reports</div>
            </div>
            
            <div class="docs-link">
                <a href="/docs">📚 View Full API Documentation</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Quantum State Visualizer",
        "version": "1.0.0",
        "endpoints": [
            "/api/quantum/simulate",
            "/api/quantum/rdm", 
            "/api/quantum/bloch",
            "/api/quantum/entanglement",
            "/api/algorithms/vqe",
            "/api/algorithms/grover",
            "/api/algorithms/qft",
            "/api/algorithms/teleport",
            "/api/chat"
        ]
    }



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
