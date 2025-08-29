#!/usr/bin/env python3
"""Test the specific circuit mentioned by the user"""
import requests
import json
import math

def test_user_circuit():
    """Test the user's specific circuit: H q[0]; H q[1];"""
    
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];"""

    print("🔬 Testing User's Circuit: H q[0]; H q[1];")
    print("Expected: |00⟩, |01⟩, |10⟩, |11⟩ all with magnitude 0.5 and 0° phase")
    print("=" * 60)
    
    try:
        # Simulate the circuit
        response = requests.post(
            'http://localhost:8002/api/quantum/simulate',
            json={'qasm': qasm, 'shots': 1000}
        )
        
        if response.ok:
            result = response.json()
            statevector = result['statevector']
            n_qubits = result['n_qubits']
            
            print(f"✅ Simulation successful: {n_qubits} qubits")
            print("\n📊 Statevector Analysis:")
            
            total_prob = 0
            for i, amp in enumerate(statevector):
                real, imag = amp[0], amp[1]
                magnitude = math.sqrt(real*real + imag*imag)
                phase_rad = math.atan2(imag, real)
                phase_deg = math.degrees(phase_rad)
                probability = magnitude * magnitude
                total_prob += probability
                
                binary_state = format(i, f'0{n_qubits}b')
                print(f"   |{binary_state}⟩ = {magnitude:.4f} ∠ {phase_deg:.1f}° = ({real:.4f} + {imag:.4f}i) → P = {probability:.4f}")
            
            print(f"\n📏 Total probability: {total_prob:.6f}")
            
            # Expected for H⊗H state: |++⟩ = (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2
            expected_magnitude = 0.5
            expected_phase = 0.0
            
            print(f"\n🎯 Verification:")
            all_correct = True
            for i, amp in enumerate(statevector):
                real, imag = amp[0], amp[1]
                magnitude = math.sqrt(real*real + imag*imag)
                phase_deg = math.degrees(math.atan2(imag, real))
                
                # Normalize phase to [0, 360)
                if phase_deg < 0:
                    phase_deg += 360
                
                binary_state = format(i, f'0{n_qubits}b')
                
                mag_correct = abs(magnitude - expected_magnitude) < 0.01
                phase_correct = abs(phase_deg - expected_phase) < 5  # 5 degree tolerance
                
                if mag_correct and phase_correct:
                    print(f"   ✅ |{binary_state}⟩ magnitude and phase correct")
                else:
                    print(f"   ❌ |{binary_state}⟩ expected {expected_magnitude:.3f}∠{expected_phase}°, got {magnitude:.3f}∠{phase_deg:.1f}°")
                    all_correct = False
            
            # Test Bloch sphere calculation
            print(f"\n🌐 Bloch Sphere Analysis:")
            bloch_response = requests.post(
                'http://localhost:8002/api/quantum/bloch',
                json={'statevector': statevector, 'n_qubits': n_qubits}
            )
            
            if bloch_response.ok:
                bloch_data = bloch_response.json()
                vectors = bloch_data['bloch_vectors']
                
                for vector in vectors:
                    x, y, z = vector['x'], vector['y'], vector['z']
                    purity = vector.get('purity', 'N/A')
                    magnitude = math.sqrt(x**2 + y**2 + z**2)
                    
                    print(f"   Qubit {vector['qubit_index']}: ({x:.3f}, {y:.3f}, {z:.3f})")
                    print(f"                    |r| = {magnitude:.3f}, purity = {purity}")
                    
                    # For |+⟩ ⊗ |+⟩ state, each qubit should point along +X axis
                    expected_bloch = (1.0, 0.0, 0.0)
                    bloch_correct = (abs(x - expected_bloch[0]) < 0.1 and 
                                   abs(y - expected_bloch[1]) < 0.1 and 
                                   abs(z - expected_bloch[2]) < 0.1)
                    
                    if bloch_correct:
                        print(f"   ✅ Qubit {vector['qubit_index']} Bloch vector correct (points to +X)")
                    else:
                        print(f"   ❌ Qubit {vector['qubit_index']} expected (1,0,0), got ({x:.3f},{y:.3f},{z:.3f})")
            else:
                print(f"   ❌ Bloch calculation failed: {bloch_response.status_code}")
            
            print(f"\n📋 Summary:")
            if all_correct:
                print("   ✅ All amplitudes have correct magnitude and phase")
                print("   ✅ Circuit simulation working correctly")
                print("   ✅ Phase information preserved and displayed")
            else:
                print("   ❌ Some amplitudes have incorrect values")
                print("   ❌ Need to investigate circuit simulation")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_user_circuit()