#!/usr/bin/env python3
"""
Debug test to identify the specific error in quantum simulation
"""

import traceback
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

def test_circuit_parsing():
    """Test circuit parsing"""
    try:
        print("Testing circuit parsing...")
        
        qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];"""
        
        circuit = QuantumCircuit.from_qasm_str(qasm)
        print(f"Circuit parsed successfully: {circuit.num_qubits} qubits")
        
        # Test removing measurements
        circuit_no_measure = circuit.copy()
        circuit_no_measure.remove_final_measurements(inplace=True)
        print(f"Circuit without measurements: {circuit_no_measure.num_qubits} qubits")
        
        # Test Statevector
        statevector_obj = Statevector(circuit_no_measure)
        statevector = statevector_obj.data
        print(f"Statevector shape: {statevector.shape}")
        
        # Test sampler
        sampler = StatevectorSampler()
        job = sampler.run([circuit], shots=1000)
        result = job.result()
        counts = result[0].data.c.get_counts()
        print(f"Counts: {counts}")
        
        return True
        
    except Exception as e:
        print(f"Error in test_circuit_parsing: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🐛 Debugging Quantum Simulation\n")
    
    success = test_circuit_parsing()
    
    if success:
        print("\n✅ Debug test passed!")
    else:
        print("\n❌ Debug test failed!")
