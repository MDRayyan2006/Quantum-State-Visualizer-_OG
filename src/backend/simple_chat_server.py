#!/usr/bin/env python3
"""
Simple Quantum Chat API - No external dependencies
Run this with: python simple_chat_server.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Quantum Chat API")

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = "quantum_education"

class ChatResponse(BaseModel):
    response: str
    context: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Educational quantum computing chatbot"""
    response_text = get_quantum_response(request.message)
    return ChatResponse(response=response_text, context=request.context)

@app.get("/")
async def root():
    return {"message": "Quantum Chat API is running", "status": "ok"}

def get_quantum_response(query: str) -> str:
    """Simple quantum computing responses"""
    q = query.lower()
    
    if any(word in q for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your Quantum Computing Assistant. Ask me about quantum gates, superposition, entanglement, or quantum algorithms!"
    
    if 'superposition' in q:
        return "Superposition allows a qubit to exist in multiple states simultaneously. A qubit can be in both |0⟩ and |1⟩ states at once, written as α|0⟩ + β|1⟩."
    
    if 'entanglement' in q:
        return "Entanglement is when qubits become correlated. The Bell state (|00⟩ + |11⟩)/√2 is a classic example where measuring one qubit instantly affects the other."
    
    if 'bloch' in q:
        return "The Bloch sphere represents qubit states geometrically. The north pole is |0⟩, south pole is |1⟩, and the equator represents superposition states."
    
    if 'hadamard' in q or 'h gate' in q:
        return "The Hadamard gate creates superposition: |0⟩ → (|0⟩ + |1⟩)/√2 and |1⟩ → (|0⟩ - |1⟩)/√2. It's the foundation of many quantum algorithms."
    
    if 'cnot' in q or 'controlled' in q:
        return "The CNOT gate creates entanglement between qubits. It flips the target qubit if the control qubit is |1⟩: |10⟩ → |11⟩, |11⟩ → |10⟩."
    
    if 'grover' in q:
        return "Grover's algorithm searches databases quadratically faster than classical methods, requiring only O(√N) steps instead of O(N)."
    
    if 'vqe' in q:
        return "VQE (Variational Quantum Eigensolver) finds ground state energies using quantum circuits and classical optimization."
    
    if 'noise' in q:
        return "Quantum noise causes decoherence and gate errors. Common models include depolarizing, amplitude damping, and phase damping."
    
    return "I'm here to help with quantum computing! Ask me about superposition, entanglement, quantum gates, or algorithms like Grover's and VQE."

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Quantum Chat API on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)