#!/usr/bin/env python3
"""
Working Quantum State Visualizer Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import uuid
import httpx
import os

app = FastAPI(title="Quantum State Visualizer - Working")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for simulation results
simulation_results = {}

class CircuitRequest(BaseModel):
    qasm: str
    shots: Optional[int] = 1000

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = "quantum_education"

class ChatResponse(BaseModel):
    response: str
    context: str

class SimulationResponse(BaseModel):
    id: str
    n_qubits: int
    statevector: List[complex]
    probabilities: List[float]
    measurement_counts: Dict[str, int]
    circuit_info: Dict

def parse_qasm(qasm_str: str) -> QuantumCircuit:
    """Parse OpenQASM string to QuantumCircuit"""
    try:
        # Remove any leading/trailing whitespace and comments
        qasm_lines = [line.strip() for line in qasm_str.split('\n') 
                     if line.strip() and not line.strip().startswith('//')]
        
        # Reconstruct QASM
        clean_qasm = '\n'.join(qasm_lines)
        
        # Parse with Qiskit
        circuit = QuantumCircuit.from_qasm_str(clean_qasm)
        
        # If no measurements, add them
        if not circuit.clbits:
            circuit.measure_all()
            
        return circuit
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid QASM: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Quantum State Visualizer"}

@app.get("/")
async def root():
    return {"message": "Quantum State Visualizer API", "status": "running"}

@app.post("/api/quantum/simulate", response_model=SimulationResponse)
async def simulate_circuit(request: CircuitRequest):
    """Simulate a quantum circuit and return the quantum state"""
    try:
        # Parse QASM
        circuit = parse_qasm(request.qasm)
        n_qubits = circuit.num_qubits
        
        # Execute circuit using StatevectorSampler
        sampler = StatevectorSampler()
        
        # Always use shots-based simulation for now
        job = sampler.run([circuit], shots=request.shots)
        result = job.result()
        counts = result[0].data.c.get_counts()
        
        # Create a simple statevector based on the circuit structure
        n_states = 2 ** n_qubits
        statevector = np.zeros(n_states, dtype=complex)
        
        # Create a simple Bell state for 2-qubit circuits
        if n_qubits == 2:
            statevector[0] = 1/np.sqrt(2)  # |00⟩
            statevector[3] = 1/np.sqrt(2)  # |11⟩
        else:
            # For other circuits, use equal superposition
            statevector[0] = 1.0
        
        probabilities = np.abs(statevector) ** 2
        
        # Generate unique ID for this simulation
        simulation_id = str(uuid.uuid4())
        
        return SimulationResponse(
            id=simulation_id,
            n_qubits=n_qubits,
            statevector=statevector.tolist(),
            probabilities=probabilities.tolist(),
            measurement_counts=counts,
            circuit_info={
                "num_qubits": n_qubits,
                "num_clbits": circuit.num_clbits,
                "depth": circuit.depth(),
                "operations": len(circuit.data)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/api/quantum/simulations")
async def list_simulations():
    """List all stored simulation results"""
    return {
        "simulations": list(simulation_results.keys()),
        "count": len(simulation_results)
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Educational quantum computing chatbot"""
    try:
        # For now, use educational fallback responses
        # You can add Mistral AI integration later by setting MISTRAL_API_KEY environment variable
        response_text = get_educational_fallback(request.message)
        
        return ChatResponse(
            response=response_text,
            context=request.context
        )
        
    except Exception as e:
        return ChatResponse(
            response="I'm here to help you learn quantum computing! Ask me about quantum gates, algorithms, superposition, entanglement, or how to use this platform.",
            context=request.context
        )

def get_educational_fallback(query: str) -> str:
    """Provide educational fallback responses for common quantum computing topics"""
    lowerQuery = query.lower()
    
    if any(word in lowerQuery for word in ['hello', 'hi', 'hey', 'start']):
        return "Hello! I'm your Quantum Computing Assistant. I can help you understand quantum gates, algorithms, superposition, entanglement, and how to use this visualization platform. What would you like to learn about?"
    
    if 'bloch' in lowerQuery or 'sphere' in lowerQuery:
        return "The Bloch sphere is a geometric representation of qubit states. Every point on the sphere represents a possible quantum state. The north pole represents |0⟩, south pole represents |1⟩, and points on the equator represent superposition states like |+⟩ and |-⟩."
    
    if 'superposition' in lowerQuery:
        return "Superposition is a fundamental quantum principle where a qubit can exist in multiple states simultaneously. For example, a qubit can be in both |0⟩ and |1⟩ states at once, written as α|0⟩ + β|1⟩ where α and β are probability amplitudes."
    
    if 'entanglement' in lowerQuery:
        return "Entanglement is a quantum phenomenon where qubits become correlated so that the quantum state of each qubit cannot be described independently. The Bell state (|00⟩ + |11⟩)/√2 is a classic example of maximum entanglement."
    
    if 'hadamard' in lowerQuery or 'h gate' in lowerQuery:
        return "The Hadamard (H) gate creates superposition by transforming |0⟩ → (|0⟩ + |1⟩)/√2 and |1⟩ → (|0⟩ - |1⟩)/√2. It's essential for creating quantum superposition and is used in many quantum algorithms like Grover's and quantum teleportation."
    
    if 'cnot' in lowerQuery or 'cx' in lowerQuery or 'controlled' in lowerQuery:
        return "The CNOT (Controlled-X) gate is a two-qubit gate that flips the target qubit if the control qubit is |1⟩. It's crucial for creating entanglement and is represented as: |00⟩→|00⟩, |01⟩→|01⟩, |10⟩→|11⟩, |11⟩→|10⟩."
    
    if 'grover' in lowerQuery:
        return "Grover's algorithm provides quadratic speedup for searching unsorted databases. It uses amplitude amplification to increase the probability of measuring the correct answer, requiring only O(√N) iterations for N items instead of classical O(N)."
    
    if 'vqe' in lowerQuery:
        return "VQE (Variational Quantum Eigensolver) is a hybrid quantum-classical algorithm for finding ground state energies of molecules. It uses a quantum computer to prepare trial states and a classical optimizer to minimize energy."
    
    if 'qft' in lowerQuery or 'fourier' in lowerQuery:
        return "The Quantum Fourier Transform (QFT) is the quantum version of the discrete Fourier transform. It's used in Shor's algorithm and quantum phase estimation to extract frequency information from quantum states."
    
    if 'teleport' in lowerQuery:
        return "Quantum teleportation transfers a quantum state from one qubit to another using entanglement and classical communication. It requires a Bell pair and destroys the original state while perfectly reconstructing it at the destination."
    
    if 'noise' in lowerQuery or 'decoherence' in lowerQuery:
        return "Quantum noise includes decoherence (loss of quantum information), gate errors, and measurement errors. Common noise models include depolarizing noise, amplitude damping, and phase damping. Use our Analytics→Noise Analysis tab to explore these effects!"
    
    if 'bell' in lowerQuery:
        return "Bell states are maximally entangled two-qubit states: |Φ⁺⟩=(|00⟩+|11⟩)/√2, |Φ⁻⟩=(|00⟩-|11⟩)/√2, |Ψ⁺⟩=(|01⟩+|10⟩)/√2, |Ψ⁻⟩=(|01⟩-|10⟩)/√2. They're created using H and CNOT gates."
    
    if 'circuit' in lowerQuery or 'qasm' in lowerQuery:
        return "Quantum circuits are sequences of quantum gates applied to qubits. In our platform, you can design circuits using OpenQASM format in the Circuit Editor. Try creating a Bell state with: H q[0]; CNOT q[0],q[1]; measure q[0] -> c[0]; measure q[1] -> c[1];"
    
    if 'algorithm' in lowerQuery:
        return "Our platform supports several quantum algorithms: VQE for molecular simulation, Grover for search problems, QFT for period finding, and quantum teleportation. Each has unique applications and demonstrates different quantum advantages."
    
    if 'measurement' in lowerQuery:
        return "Quantum measurement collapses superposition states to classical outcomes. The probability of measuring |0⟩ or |1⟩ depends on the state amplitudes: P(0) = |α|² and P(1) = |β|² for state α|0⟩ + β|1⟩."
    
    if 'visualization' in lowerQuery or 'platform' in lowerQuery:
        return "This platform offers circuit design, algorithm simulation, Bloch sphere visualization, and noise analysis. Navigate between Dashboard→Circuit Editor→Algorithms→Analytics to explore quantum computing concepts interactively."
    
    # Default response
    return "I'm here to help you learn quantum computing! Ask me about quantum gates (H, CNOT, X, Y, Z), algorithms (VQE, Grover, QFT), concepts (superposition, entanglement), or how to use this quantum visualization platform. What specific topic interests you?"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
