#!/usr/bin/env python3
"""
Test Qiskit imports to debug the import issues
"""

print("Testing Qiskit imports...")

try:
    import qiskit
    print("✅ qiskit imported successfully")
    print(f"   Version: {getattr(qiskit, '__version__', 'unknown')}")
except Exception as e:
    print(f"❌ qiskit import failed: {e}")

try:
    from qiskit import QuantumCircuit
    print("✅ QuantumCircuit imported successfully")
except Exception as e:
    print(f"❌ QuantumCircuit import failed: {e}")

try:
    from qiskit_aer import AerSimulator
    print("✅ AerSimulator imported successfully")
except Exception as e:
    print(f"❌ AerSimulator import failed: {e}")

try:
    from qiskit.quantum_info import Statevector
    print("✅ Statevector imported successfully")
except Exception as e:
    print(f"❌ Statevector import failed: {e}")

try:
    from qiskit.quantum_info import DensityMatrix
    print("✅ DensityMatrix imported successfully")
except Exception as e:
    print(f"❌ DensityMatrix import failed: {e}")

# Test creating a simple circuit
try:
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    print("✅ Basic circuit creation works")
    print(f"   Circuit: {circuit}")
except Exception as e:
    print(f"❌ Circuit creation failed: {e}")

print("\nTest completed!")