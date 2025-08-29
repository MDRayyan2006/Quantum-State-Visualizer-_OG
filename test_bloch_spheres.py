#!/usr/bin/env python3
"""
Test script to verify the updated Bloch vector calculations
"""

import requests
import json
import time

BASE_URL = "http://localhost:8002"

def test_bloch_sphere_visualization():
    """Test the Bloch sphere visualization with various quantum circuits"""
    
    print("🧪 Testing Bloch Sphere Visualization...")
    
    test_cases = [
        {
            "name": "Single Qubit |0⟩ State",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
measure q[0] -> c[0];""",
            "expected_qubits": 1,
            "expected_z": [1.0]  # |0⟩ should be at north pole
        },
        {
            "name": "Single Qubit |1⟩ State", 
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
x q[0];
measure q[0] -> c[0];""",
            "expected_qubits": 1,
            "expected_z": [-1.0]  # |1⟩ should be at south pole
        },
        {
            "name": "Single Qubit |+⟩ State",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
measure q[0] -> c[0];""",
            "expected_qubits": 1,
            "expected_z": [0.0],  # |+⟩ should be on equator
            "expected_x": [1.0]   # along +X axis
        },
        {
            "name": "Single Qubit |-⟩ State",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
z q[0];
measure q[0] -> c[0];""",
            "expected_qubits": 1,
            "expected_z": [0.0],  # |-⟩ should be on equator
            "expected_x": [-1.0],  # along -X axis
            "description": "|-⟩ state should show negative X component"
        },
        {
            "name": "Single Qubit |+i⟩ State", 
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
s q[0];
measure q[0] -> c[0];""",
            "expected_qubits": 1,
            "expected_z": [0.0],  # |+i⟩ should be on equator
            "expected_y": [1.0],   # along +Y axis
            "description": "S gate should create |+i⟩ state with Y component"
        },
        {
            "name": "Bell State (2 Qubits)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];""",
            "expected_qubits": 2,
            "description": "Bell state should show entangled qubits"
        },
        {
            "name": "GHZ State (3 Qubits)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
cx q[0],q[1];
cx q[1],q[2];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];""",
            "expected_qubits": 3,
            "description": "GHZ state should show 3 entangled qubits"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🔬 Test {i+1}: {test_case['name']}")
        print(f"   Description: {test_case.get('description', 'Testing Bloch vector calculation')}")
        
        try:
            # Simulate the circuit
            sim_response = requests.post(f"{BASE_URL}/api/quantum/simulate", 
                json={"qasm": test_case["qasm"], "shots": 1024}, 
                timeout=10)
            
            if not sim_response.ok:
                print(f"❌ Simulation failed: {sim_response.status_code}")
                print(f"   Error: {sim_response.text}")
                continue
                
            sim_data = sim_response.json()
            print(f"✅ Simulation successful: {sim_data['n_qubits']} qubits")
            
            # Calculate Bloch vectors
            bloch_response = requests.post(f"{BASE_URL}/api/quantum/bloch",
                json={
                    "statevector": sim_data["statevector"],
                    "n_qubits": sim_data["n_qubits"]
                },
                timeout=10)
            
            if not bloch_response.ok:
                print(f"❌ Bloch calculation failed: {bloch_response.status_code}")
                print(f"   Error: {bloch_response.text}")
                continue
                
            bloch_data = bloch_response.json()
            vectors = bloch_data["bloch_vectors"]
            
            print(f"✅ Bloch vectors calculated for {len(vectors)} qubits:")
            
            for j, vector in enumerate(vectors):
                x, y, z = vector["x"], vector["y"], vector["z"]
                purity = vector.get("purity", "N/A")
                magnitude = (x**2 + y**2 + z**2)**0.5
                
                print(f"   Qubit {j}: ({x:.3f}, {y:.3f}, {z:.3f})")
                print(f"            |r| = {magnitude:.3f}, purity = {purity}")
                
                # Check expectations if provided
                if "expected_qubits" in test_case and len(vectors) != test_case["expected_qubits"]:
                    print(f"⚠️  Expected {test_case['expected_qubits']} qubits, got {len(vectors)}")
                
                if "expected_z" in test_case and j < len(test_case["expected_z"]):
                    expected_z = test_case["expected_z"][j]
                    if abs(z - expected_z) > 0.1:
                        print(f"⚠️  Expected z ≈ {expected_z}, got {z:.3f}")
                    else:
                        print(f"✅ Z component matches expectation: {expected_z} ≈ {z:.3f}")
                
                if "expected_x" in test_case and j < len(test_case["expected_x"]):
                    expected_x = test_case["expected_x"][j]
                    if abs(x - expected_x) > 0.1:
                        print(f"⚠️  Expected x ≈ {expected_x}, got {x:.3f}")
                    else:
                        print(f"✅ X component matches expectation: {expected_x} ≈ {x:.3f}")
                
                if "expected_y" in test_case and j < len(test_case["expected_y"]):
                    expected_y = test_case["expected_y"][j]
                    if abs(y - expected_y) > 0.1:
                        print(f"⚠️  Expected y ≈ {expected_y}, got {y:.3f}")
                    else:
                        print(f"✅ Y component matches expectation: {expected_y} ≈ {y:.3f}")
            
            # Summary for this test
            print(f"📊 Test Summary:")
            print(f"   - {len(vectors)} individual Bloch spheres will be displayed")
            print(f"   - Each qubit has its own reduced density matrix")
            print(f"   - Purity values indicate entanglement/mixing")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.ok:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Updated Bloch Sphere Visualization")
    print("=" * 60)
    
    if test_api_health():
        test_bloch_sphere_visualization()
        
        print("\n" + "=" * 60)
        print("🎉 Testing Complete!")
        print("\n📋 Summary of Changes:")
        print("   ✅ Backend now uses Statevector.from_instruction()")
        print("   ✅ Individual reduced density matrices for each qubit")
        print("   ✅ Separate Bloch sphere for each qubit in frontend")
        print("   ✅ Correct Bloch vector calculations with proper signs")
        print("   ✅ Purity calculation for entanglement detection")
        
        print("\n🔗 View the updated visualization at:")
        print("   Frontend: http://localhost:3000")
        print("   Circuit Editor: http://localhost:3000/circuit-editor")
        print("   Algorithms: http://localhost:3000/algorithms")
    else:
        print("❌ Cannot test - API is not running")
        print("💡 Start the backend with: python -m uvicorn main:app --host 0.0.0.0 --port 8002")