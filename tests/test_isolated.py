#!/usr/bin/env python3
"""
Minimal test to isolate the Statevector error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    
    # Test basic imports
    from fastapi import APIRouter
    print("✅ FastAPI imported")
    
    from qiskit import QuantumCircuit
    print("✅ QuantumCircuit imported")
    
    from qiskit.primitives import StatevectorSampler
    print("✅ StatevectorSampler imported")
    
    # Test creating a simple circuit
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    print("✅ Circuit created")
    
    # Test StatevectorSampler
    sampler = StatevectorSampler()
    print("✅ Sampler created")
    
    # Test running the circuit
    job = sampler.run([circuit], shots=1000)
    result = job.result()
    counts = result[0].data.c.get_counts()
    print(f"✅ Simulation successful: {counts}")
    
    print("\n🎉 All tests passed! No Statevector error found.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
