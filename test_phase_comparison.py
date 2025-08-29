#!/usr/bin/env python3
"""Test to show the difference between circuits with and without phases"""
import requests
import json
import math

def test_phase_comparison():
    """Compare circuits that do and don't have 45° phases"""
    
    test_cases = [
        {
            "name": "H⊗H Circuit (User's Original) - No 45° phases",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];""",
            "explanation": "Creates |++⟩ state with all real amplitudes (0° phases)",
            "expected_behavior": "All amplitudes should show 0° phase, Bloch vectors (1,0,0)"
        },
        {
            "name": "H+T⊗H Circuit - Actual 45° phases",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
t q[0];
h q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];""",
            "explanation": "T gate adds π/4 phase to |1⟩ component of first qubit",
            "expected_behavior": "First qubit: |0⟩=0°, |1⟩=45°; Second qubit: |0⟩=0°, |1⟩=0°"
        },
        {
            "name": "H+T⊗H+T Circuit - Both qubits with 45° phases",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
t q[0];
h q[1];
t q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];""",
            "explanation": "T gates on both qubits create phase combinations",
            "expected_behavior": "|00⟩=0°, |01⟩=45°, |10⟩=45°, |11⟩=90°"
        }
    ]
    
    print("🎯 Phase Comparison Test: Circuits With and Without 45° Phases")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🔬 Test {i+1}: {test_case['name']}")
        print(f"   📝 {test_case['explanation']}")
        print(f"   🎯 Expected: {test_case['expected_behavior']}")
        
        try:
            # Simulate the circuit
            response = requests.post(
                'http://localhost:8003/api/quantum/simulate',
                json={'qasm': test_case['qasm'], 'shots': 1000}
            )
            
            if response.ok:
                result = response.json()
                statevector = result['statevector']
                n_qubits = result['n_qubits']
                
                print(f"   ✅ Simulation successful: {n_qubits} qubits")
                print(f"   📊 Statevector Analysis:")
                
                # Analyze phases
                phase_found = {"0°": 0, "45°": 0, "90°": 0, "others": 0}
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
                        
                        # Count phases
                        if abs(phase_deg - 0) < 5 or abs(phase_deg - 360) < 5:
                            phase_found["0°"] += 1
                        elif abs(phase_deg - 45) < 5:
                            phase_found["45°"] += 1
                        elif abs(phase_deg - 90) < 5:
                            phase_found["90°"] += 1
                        else:
                            phase_found["others"] += 1
                
                # Test Bloch sphere calculation
                print(f"   🌐 Bloch Sphere Analysis:")
                bloch_response = requests.post(
                    'http://localhost:8003/api/quantum/bloch',
                    json={'statevector': statevector, 'n_qubits': n_qubits}
                )
                
                if bloch_response.ok:
                    bloch_data = bloch_response.json()
                    vectors = bloch_data['bloch_vectors']
                    
                    for vector in vectors:
                        x, y, z = vector['x'], vector['y'], vector['z']
                        purity = vector.get('purity', 'N/A')
                        magnitude = math.sqrt(x**2 + y**2 + z**2)
                        
                        print(f"     Qubit {vector['qubit_index']}: ({x:.3f}, {y:.3f}, {z:.3f})")
                        print(f"                         |r| = {magnitude:.3f}, purity = {purity}")
                        
                        # Check if Bloch vector magnitude is correct
                        if abs(magnitude - 1.0) < 0.1:
                            print(f"       ✅ Correct Bloch vector magnitude")
                        else:
                            print(f"       ❌ Expected |r| ≈ 1.0, got {magnitude:.3f}")
                else:
                    print(f"     ❌ Bloch calculation failed")
                
                # Summary
                print(f"   📋 Phase Summary:")
                print(f"     0° phases: {phase_found['0°']}")
                print(f"     45° phases: {phase_found['45°']}")
                print(f"     90° phases: {phase_found['90°']}")
                print(f"     Other phases: {phase_found['others']}")
                
                if phase_found["45°"] > 0:
                    print(f"     ✅ This circuit DOES produce 45° phases!")
                else:
                    print(f"     ❌ This circuit does NOT produce 45° phases")
                    
            else:
                print(f"   ❌ Simulation failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 Phase Comparison Test Complete!")
    print("\n📋 Key Findings:")
    print("   1. H⊗H circuit produces 0° phases (all real amplitudes)")
    print("   2. For actual 45° phases, you need T gates or explicit phase rotations")
    print("   3. T gate adds π/4 (45°) phase to |1⟩ component")
    print("   4. Multiple T gates create phase combinations (0°, 45°, 90°)")
    print("   5. Bloch vectors now correctly show magnitude 1.0 for pure states")
    
    print("\n🚀 To see 45° phases in your circuit, try:")
    print("   H q[0]; T q[0]; H q[1]; T q[1];")
    print("   This will create: |00⟩=0°, |01⟩=45°, |10⟩=45°, |11⟩=90°")

if __name__ == "__main__":
    test_phase_comparison()