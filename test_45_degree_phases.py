#!/usr/bin/env python3
"""Test circuits that actually produce 45° phases"""
import requests
import json
import math

def test_circuits_with_45_phases():
    """Test circuits that should produce 45° phases"""
    
    test_cases = [
        {
            "name": "H⊗H Circuit (Your Original)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];""",
            "expected_phases_deg": [0, 0, 0, 0],  # All real, 0° phases
            "note": "H⊗H produces |++⟩ state with all real amplitudes"
        },
        {
            "name": "Single Qubit with T Gate (45° phase)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
t q[0];
measure q[0] -> c[0];""",
            "expected_phases_deg": [0, 45],  # |0⟩: 0°, |1⟩: 45°
            "note": "T gate adds π/4 phase to |1⟩ component"
        },
        {
            "name": "Two Qubits with T Gates (45° phases)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
t q[0];
t q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];""",
            "expected_phases_deg": [0, 45, 45, 90],  # |00⟩: 0°, |01⟩: 45°, |10⟩: 45°, |11⟩: 90°
            "note": "T gates on both qubits create phase combinations"
        },
        {
            "name": "Phase Gate Circuit (π/4 = 45°)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
p(pi/4) q[0];
measure q[0] -> c[0];""",
            "expected_phases_deg": [0, 45],
            "note": "Explicit π/4 phase gate for 45° phase"
        }
    ]
    
    print("🔬 Testing Circuits for 45° Phase Analysis")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases):
        print(f"\n📊 Test {i+1}: {test_case['name']}")
        print(f"   Note: {test_case['note']}")
        
        try:
            response = requests.post(
                'http://localhost:8002/api/quantum/simulate',
                json={'qasm': test_case['qasm'], 'shots': 1000}
            )
            
            if response.ok:
                result = response.json()
                statevector = result['statevector']
                n_qubits = result['n_qubits']
                
                print(f"✅ Simulation successful: {n_qubits} qubits")
                print(f"   Statevector Analysis:")
                
                has_45_phases = False
                for j, amp in enumerate(statevector):
                    real, imag = amp[0], amp[1]
                    magnitude = math.sqrt(real*real + imag*imag)
                    
                    if magnitude > 1e-10:  # Non-zero amplitude
                        phase_rad = math.atan2(imag, real)
                        phase_deg = math.degrees(phase_rad)
                        
                        # Normalize phase to [0, 360)
                        if phase_deg < 0:
                            phase_deg += 360
                            
                        binary_state = format(j, f'0{n_qubits}b')
                        print(f"     |{binary_state}⟩ = {magnitude:.4f} ∠ {phase_deg:.1f}° = ({real:.4f} + {imag:.4f}i)")
                        
                        # Check for 45° phases
                        if abs(phase_deg - 45) < 5 or abs(phase_deg - 225) < 5:  # ±45°
                            has_45_phases = True
                            print(f"       ✅ Found 45° phase!")
                
                if has_45_phases:
                    print(f"   ✅ This circuit DOES produce 45° phases")
                else:
                    print(f"   ❌ This circuit does NOT produce 45° phases")
                    
                # Test Bloch sphere calculation
                print(f"   Bloch Sphere Analysis:")
                bloch_response = requests.post(
                    'http://localhost:8002/api/quantum/bloch',
                    json={'statevector': statevector, 'n_qubits': n_qubits}
                )
                
                if bloch_response.ok:
                    bloch_data = bloch_response.json()
                    vectors = bloch_data['bloch_vectors']
                    
                    for vector in vectors:
                        x, y, z = vector['x'], vector['y'], vector['z']
                        magnitude = math.sqrt(x**2 + y**2 + z**2)
                        print(f"     Qubit {vector['qubit_index']}: ({x:.3f}, {y:.3f}, {z:.3f}) |r| = {magnitude:.3f}")
                        
                        # For individual qubits in superposition, expect |r| = 1.0
                        if abs(magnitude - 1.0) < 0.1:
                            print(f"       ✅ Correct Bloch vector magnitude")
                        else:
                            print(f"       ❌ Expected |r| ≈ 1.0, got {magnitude:.3f}")
                else:
                    print(f"     ❌ Bloch calculation failed")
                    
            else:
                print(f"❌ Simulation failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("📋 Summary:")
    print("   🔍 H⊗H circuit produces 0° phases (all real amplitudes)")
    print("   🔍 For 45° phases, use T gates or explicit phase gates")
    print("   🔍 Bloch vector magnitudes should be 1.0 for pure single-qubit states")
    print("   🔍 Current issue: Bloch vectors showing 0.5 magnitude instead of 1.0")

if __name__ == "__main__":
    test_circuits_with_45_phases()