#!/usr/bin/env python3
"""
Debug the circuit without measurements issue locally
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

def test_circuit_without_measurements():
    print("🔬 Local debugging of circuit without measurements")
    
    # Create a circuit without measurements  
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];"""
    
    try:
        print("📝 Creating circuit from QASM...")
        circuit = QuantumCircuit.from_qasm_str(qasm)
        print(f"✅ Original circuit: {circuit.num_qubits} qubits, {circuit.num_clbits} classical bits")
        
        # This is what the parse_qasm function does:
        if not circuit.clbits:
            print("⚠️ No classical bits found, adding measurements...")
            circuit.measure_all()
            print(f"✅ After measure_all(): {circuit.num_qubits} qubits, {circuit.num_clbits} classical bits")
        
        # Test statevector simulation
        print("🧮 Creating statevector circuit...")
        statevector_circuit = circuit.copy()
        statevector_circuit.remove_final_measurements()
        print(f"📊 Statevector circuit: {statevector_circuit.num_qubits} qubits, {statevector_circuit.num_clbits} classical bits")
        
        print("🎯 Getting statevector...")
        statevector = Statevector(statevector_circuit)
        statevector_data = statevector.data
        print(f"✅ Statevector calculated: {statevector_data}")
        
        print("📏 Calculating probabilities...")
        import numpy as np
        probabilities = np.abs(statevector_data) ** 2
        print(f"✅ Probabilities: {probabilities}")
        
        # Test measurement simulation  
        print("🎲 Testing measurement simulation...")
        sampler = StatevectorSampler()
        job = sampler.run([circuit], shots=1000)
        result = job.result()
        print(f"✅ Job completed")
        
        try:
            counts = result[0].data.c.get_counts()
            print(f"✅ Counts: {counts}")
        except Exception as e:
            print(f"❌ Failed to get counts: {e}")
            # Create synthetic counts
            counts = {}
            for i, prob in enumerate(probabilities):
                if prob > 1e-10:
                    binary_state = format(i, f'0{circuit.num_qubits}b')
                    expected_count = int(prob * 1000)
                    if expected_count > 0:
                        counts[binary_state] = expected_count
            print(f"🔄 Synthetic counts: {counts}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_circuit_without_measurements()