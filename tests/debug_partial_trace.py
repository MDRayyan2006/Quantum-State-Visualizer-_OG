#!/usr/bin/env python3
"""Debug the partial trace issue in Bloch vector calculation"""

import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

def debug_partial_trace():
    """Debug partial trace for H⊗H state"""
    
    # Create H⊗H state manually: |++⟩ = (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2
    statevector = np.array([0.5, 0.5, 0.5, 0.5], dtype=complex)
    print("🔬 Debugging H⊗H state: |++⟩")
    print(f"Statevector: {statevector}")
    
    # Create quantum state objects
    state = Statevector(statevector)
    full_dm = DensityMatrix(state)
    
    print(f"\n📊 Full density matrix (2x2 = 4x4):")
    print(f"Shape: {full_dm.data.shape}")
    print(f"Diagonal: {np.diag(full_dm.data)}")
    
    # For |++⟩ state, the density matrix should be:
    # ρ = |++⟩⟨++| = (|00⟩ + |01⟩ + |10⟩ + |11⟩)(⟨00| + ⟨01| + ⟨10| + ⟨11|) / 4
    expected_dm = np.ones((4,4), dtype=complex) * 0.25
    print(f"\n🎯 Expected density matrix for |++⟩:")
    print(expected_dm)
    print(f"Actual density matrix:")
    print(full_dm.data)
    
    # Now test partial trace for each qubit
    print(f"\n🧮 Testing partial trace for individual qubits:")
    
    # Qubit 0: trace out qubit 1
    print(f"\n📊 Qubit 0 (trace out qubit 1):")
    try:
        rdm_0 = partial_trace(full_dm, [1])  # trace out qubit 1
        print(f"Shape: {rdm_0.data.shape}")
        print(f"Reduced density matrix:")
        print(rdm_0.data)
        
        # For |+⟩ state, RDM should be [[0.5, 0.5], [0.5, 0.5]]
        expected_rdm_plus = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
        print(f"Expected for |+⟩ state:")
        print(expected_rdm_plus)
        
        # Calculate Bloch vector
        pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
        pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        rho = rdm_0.data
        x = float(np.real(np.trace(rho @ pauli_x)))
        y = float(np.real(np.trace(rho @ pauli_y)))
        z = float(np.real(np.trace(rho @ pauli_z)))
        magnitude = np.sqrt(x**2 + y**2 + z**2)
        
        print(f"Bloch vector: ({x:.3f}, {y:.3f}, {z:.3f})")
        print(f"Magnitude: {magnitude:.3f}")
        print(f"Expected: (1.000, 0.000, 0.000) with magnitude 1.000")
        
        if abs(magnitude - 1.0) < 0.1:
            print("✅ Correct magnitude!")
        else:
            print("❌ Incorrect magnitude!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Qubit 1: trace out qubit 0
    print(f"\n📊 Qubit 1 (trace out qubit 0):")
    try:
        rdm_1 = partial_trace(full_dm, [0])  # trace out qubit 0
        print(f"Shape: {rdm_1.data.shape}")
        print(f"Reduced density matrix:")
        print(rdm_1.data)
        
        # Calculate Bloch vector
        rho = rdm_1.data
        x = float(np.real(np.trace(rho @ pauli_x)))
        y = float(np.real(np.trace(rho @ pauli_y)))
        z = float(np.real(np.trace(rho @ pauli_z)))
        magnitude = np.sqrt(x**2 + y**2 + z**2)
        
        print(f"Bloch vector: ({x:.3f}, {y:.3f}, {z:.3f})")
        print(f"Magnitude: {magnitude:.3f}")
        print(f"Expected: (1.000, 0.000, 0.000) with magnitude 1.000")
        
        if abs(magnitude - 1.0) < 0.1:
            print("✅ Correct magnitude!")
        else:
            print("❌ Incorrect magnitude!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n📋 Analysis:")
    print(f"   - H⊗H creates |++⟩ state where each qubit is in |+⟩ state")
    print(f"   - Each individual qubit should have Bloch vector (1,0,0)")
    print(f"   - Reduced density matrix for |+⟩ should be [[0.5, 0.5], [0.5, 0.5]]")
    print(f"   - If magnitude is 0.5 instead of 1.0, partial trace is incorrect")

if __name__ == "__main__":
    debug_partial_trace()