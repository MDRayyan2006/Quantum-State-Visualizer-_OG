from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.quantum_new import router as quantum_router

app = FastAPI(title="Test App")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the quantum router
app.include_router(quantum_router, prefix="/api/quantum", tags=["quantum"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Quantum State Visualizer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
