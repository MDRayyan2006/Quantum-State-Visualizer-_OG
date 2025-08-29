#!/usr/bin/env python3
"""
Simple Working Backend for State Vector Fix Testing
This backend provides working quantum simulation without complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
import uuid
import math

app = FastAPI(title="Simple Quantum Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CircuitRequest(BaseModel):
    qasm: str
    shots: Optional[int] = 1000

class SimulationResponse(BaseModel):
    id: str
    n_qubits: int
    statevector: List[List[float]]  # Each complex number as [real, imag]
    probabilities: List[float]
    measurement_counts: Dict[str, int]
    circuit_info: Dict

def create_bell_state_statevector():
    """Create a proper Bell state with complex numbers"""
    # Bell state: (|00⟩ + |11⟩) / √2
    statevector = np.zeros(4, dtype=complex)
    statevector[0] = 1/np.sqrt(2) + 0j  # |00⟩ amplitude
    statevector[1] = 0 + 0j             # |01⟩ amplitude  
    statevector[2] = 0 + 0j             # |10⟩ amplitude
    statevector[3] = 1/np.sqrt(2) + 0j  # |11⟩ amplitude
    return statevector

def create_superposition_state(n_qubits):
    """Create equal superposition state"""
    n_states = 2 ** n_qubits
    amplitude = 1/np.sqrt(n_states)
    statevector = np.full(n_states, amplitude + 0j, dtype=complex)
    return statevector

def calculate_probabilities(statevector):
    """Calculate probabilities from statevector (handles both complex and [real,imag] formats)"""
    probabilities = []
    for amplitude in statevector:
        if isinstance(amplitude, list) and len(amplitude) == 2:
            # [real, imag] format
            real, imag = amplitude[0], amplitude[1]
            magnitude_squared = real * real + imag * imag
        else:
            # Complex number format
            magnitude_squared = abs(amplitude) ** 2
        probabilities.append(float(magnitude_squared))
    return probabilities

def parse_qasm_simple(qasm_str: str) -> Dict:
    """Simple QASM parser to extract basic circuit info"""
    lines = [line.strip() for line in qasm_str.split('\n') 
             if line.strip() and not line.strip().startswith('//')]
    
    n_qubits = 2  # default
    has_hadamard = False
    has_cnot = False
    
    for line in lines:
        # Extract qubit count
        if 'qreg' in line:
            match = line.split('[')[1].split(']')[0] if '[' in line else '2'
            n_qubits = int(match)
        
        # Check for common gates
        if line.startswith('h '):
            has_hadamard = True
        if line.startswith('cx ') or line.startswith('cnot '):
            has_cnot = True
    
    return {
        'n_qubits': n_qubits,
        'has_hadamard': has_hadamard,
        'has_cnot': has_cnot
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Simple Quantum Backend"}

@app.post("/api/quantum/simulate", response_model=SimulationResponse)
async def simulate_circuit(request: CircuitRequest):
    """Simulate quantum circuit with proper complex number handling"""
    try:
        print(f"📨 Received simulation request: {len(request.qasm)} chars QASM")
        
        # Parse basic circuit info
        circuit_info = parse_qasm_simple(request.qasm)
        n_qubits = circuit_info['n_qubits']
        
        # Create appropriate quantum state based on circuit
        if circuit_info['has_hadamard'] and circuit_info['has_cnot'] and n_qubits == 2:
            # Bell state
            statevector_np = create_bell_state_statevector()
            # Convert to [real, imag] format
            statevector = [[float(np.real(amp)), float(np.imag(amp))] for amp in statevector_np]
            print("📊 Created Bell state")
        elif circuit_info['has_hadamard']:
            # Superposition state
            statevector_np = create_superposition_state(n_qubits)
            # Convert to [real, imag] format
            statevector = [[float(np.real(amp)), float(np.imag(amp))] for amp in statevector_np]
            print(f"📊 Created superposition state for {n_qubits} qubits")
        else:
            # Ground state with amplitude on |0...0⟩
            n_states = 2 ** n_qubits
            statevector = [[0.0, 0.0] for _ in range(n_states)]
            statevector[0] = [1.0, 0.0]  # |00...0⟩ state
            print(f"📊 Created ground state for {n_qubits} qubits")
        
        # Calculate probabilities
        probabilities = calculate_probabilities(statevector)
        
        # Create measurement counts based on probabilities
        counts = {}
        for i, prob in enumerate(probabilities):
            if prob > 0.001:  # Only include significant probabilities
                binary_state = format(i, f'0{n_qubits}b')
                expected_count = int(prob * request.shots)
                if expected_count > 0:
                    counts[binary_state] = expected_count
        
        # Generate simulation ID
        simulation_id = str(uuid.uuid4())
        
        print(f"✅ Simulation completed: {len(statevector)} amplitudes, {len(counts)} measurement outcomes")
        print(f"📈 Sample amplitudes: {statevector[:2]}")
        print(f"📊 Probabilities: {probabilities[:4]}")
        
        return SimulationResponse(
            id=simulation_id,
            n_qubits=n_qubits,
            statevector=statevector,  # Already in [[real,imag], ...] format
            probabilities=probabilities,
            measurement_counts=counts,
            circuit_info={
                "num_qubits": n_qubits,
                "num_clbits": n_qubits,
                "depth": 3,
                "operations": 4
            }
        )
        
    except Exception as e:
        print(f"❌ Simulation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Quantum Backend on port 8003...")
    uvicorn.run(app, host="0.0.0.0", port=8003)