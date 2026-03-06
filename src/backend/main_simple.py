from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.quantum import router as quantum_router

app = FastAPI(title="Quantum State Visualizer - Simple")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the quantum router
app.include_router(quantum_router, prefix="/api/quantum", tags=["quantum"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Quantum State Visualizer"}

@app.get("/")
async def root():
    return {"message": "Quantum State Visualizer API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
