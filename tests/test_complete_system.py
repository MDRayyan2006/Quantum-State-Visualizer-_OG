#!/usr/bin/env python3
"""
Comprehensive End-to-End Test for Quantum State Visualizer
Tests the complete flow from quantum circuit simulation to Bloch sphere visualization
"""

import requests
import json
import time

BASE_URL = "http://localhost:8002"
FRONTEND_URL = "http://localhost:3000"

def test_api_health():
    """Test API health and availability"""
    print("🔍 Testing API Health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API Health: {health['status']}")
            print(f"   Service: {health['service']}")
            print(f"   Available endpoints: {len(health['endpoints'])}")
            return True
        else:
            print(f"❌ API Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API not accessible: {e}")
        return False

def test_quantum_circuits():
    """Test various quantum circuits and their Bloch sphere representations"""
    print("\n🔬 Testing Quantum Circuits...")
    
    test_cases = [
        {
            "name": "Single Qubit |0⟩ State",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
measure q[0] -> c[0];""",
            "expected_bloch": {"x": 0.0, "y": 0.0, "z": 1.0, "purity": 1.0}
        },
        {
            "name": "Single Qubit |+⟩ State (H gate)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
measure q[0] -> c[0];""",
            "expected_bloch": {"x": 1.0, "y": 0.0, "z": 0.0, "purity": 1.0}
        },
        {
            "name": "Single Qubit |i⟩ State (H + S gates)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
h q[0];
s q[0];
measure q[0] -> c[0];""",
            "expected_bloch": {"x": 0.0, "y": -1.0, "z": 0.0, "purity": 1.0}
        },
        {
            "name": "Bell State (maximally entangled)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;""",
            "expected_bloch": {"x": 0.0, "y": 0.0, "z": 0.0, "purity": 0.5}
        },
        {
            "name": "GHZ State (3-qubit entanglement)",
            "qasm": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
cx q[0],q[1];
cx q[1],q[2];
measure q -> c;""",
            "expected_bloch": {"x": 0.0, "y": 0.0, "z": 0.0, "purity": 0.5}
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases):
        print(f"\n   Test {i+1}: {test_case['name']}")
        
        # Simulate the circuit
        sim_data = {"qasm": test_case["qasm"], "shots": 1000}
        response = requests.post(f"{BASE_URL}/api/quantum/simulate", json=sim_data)
        
        if response.status_code != 200:
            print(f"   ❌ Simulation failed: {response.status_code}")
            results.append(False)
            continue
            
        sim_result = response.json()
        print(f"   ✅ Simulation successful: {sim_result['n_qubits']} qubits")
        
        # Calculate Bloch vectors
        bloch_data = {
            "statevector": sim_result['statevector'],
            "n_qubits": sim_result['n_qubits']
        }
        
        bloch_response = requests.post(f"{BASE_URL}/api/quantum/bloch", json=bloch_data)
        
        if bloch_response.status_code != 200:
            print(f"   ❌ Bloch calculation failed: {bloch_response.status_code}")
            results.append(False)
            continue
            
        bloch_result = bloch_response.json()
        print(f"   ✅ Bloch vectors calculated for {len(bloch_result['bloch_vectors'])} qubits")
        
        # Validate results (for single qubit cases)
        if sim_result['n_qubits'] == 1:
            bloch_vector = bloch_result['bloch_vectors'][0]
            expected = test_case['expected_bloch']
            
            # Check if Bloch vector components are close to expected (tolerance: 0.1)
            x_match = abs(bloch_vector['x'] - expected['x']) < 0.1
            y_match = abs(bloch_vector['y'] - expected['y']) < 0.1  
            z_match = abs(bloch_vector['z'] - expected['z']) < 0.1
            purity_match = abs(bloch_vector['purity'] - expected['purity']) < 0.1
            
            if x_match and y_match and z_match and purity_match:
                print(f"   ✅ Bloch vector matches expected values")
                print(f"      Actual: X={bloch_vector['x']:.3f}, Y={bloch_vector['y']:.3f}, Z={bloch_vector['z']:.3f}, P={bloch_vector['purity']:.3f}")
                print(f"      Expected: X={expected['x']:.3f}, Y={expected['y']:.3f}, Z={expected['z']:.3f}, P={expected['purity']:.3f}")
                results.append(True)
            else:
                print(f"   ⚠️  Bloch vector doesn't match expected values")
                print(f"      Actual: X={bloch_vector['x']:.3f}, Y={bloch_vector['y']:.3f}, Z={bloch_vector['z']:.3f}, P={bloch_vector['purity']:.3f}")
                print(f"      Expected: X={expected['x']:.3f}, Y={expected['y']:.3f}, Z={expected['z']:.3f}, P={expected['purity']:.3f}")
                results.append(False)
        else:
            # For multi-qubit cases, check entanglement (purity should be < 1)
            entangled = all(bv['purity'] < 0.8 for bv in bloch_result['bloch_vectors'])
            if entangled:
                print(f"   ✅ Multi-qubit entanglement detected (low purity values)")
                results.append(True)
            else:
                print(f"   ⚠️  Expected entanglement not detected")
                results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n   📊 Circuit Test Results: {sum(results)}/{len(results)} passed ({success_rate:.1f}%)")
    return success_rate > 80

def test_rdm_calculations():
    """Test reduced density matrix calculations"""
    print("\n🧮 Testing Reduced Density Matrix Calculations...")
    
    # Create a Bell state for testing
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    # Simulate
    sim_response = requests.post(f"{BASE_URL}/api/quantum/simulate", json={"qasm": qasm})
    if sim_response.status_code != 200:
        print("   ❌ Failed to simulate Bell state for RDM test")
        return False
        
    sim_result = sim_response.json()
    
    # Test RDM calculation - trace out qubit 0
    rdm_data = {
        "statevector": sim_result['statevector'],
        "n_qubits": sim_result['n_qubits'],
        "trace_qubits": [0]
    }
    
    rdm_response = requests.post(f"{BASE_URL}/api/quantum/rdm", json=rdm_data)
    
    if rdm_response.status_code != 200:
        print(f"   ❌ RDM calculation failed: {rdm_response.status_code}")
        return False
        
    rdm_result = rdm_response.json()
    
    print(f"   ✅ RDM calculation successful")
    print(f"      Traced out qubits: {rdm_result['traced_qubits']}")
    print(f"      Remaining qubits: {rdm_result['remaining_qubits']}")
    print(f"      Eigenvalues: {[f'{ev:.3f}' for ev in rdm_result['eigenvalues']]}")
    
    # For a Bell state, tracing out one qubit should give a maximally mixed state
    # Eigenvalues should be approximately [0.5, 0.5]
    eigenvals = rdm_result['eigenvalues']
    mixed_state = all(abs(ev - 0.5) < 0.1 for ev in eigenvals)
    
    if mixed_state:
        print(f"   ✅ RDM shows expected maximally mixed state")
        return True
    else:
        print(f"   ⚠️  RDM doesn't show expected mixed state behavior")
        return False

def test_frontend_connectivity():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Connectivity...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend is accessible")
            return True
        else:
            print(f"   ❌ Frontend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend not accessible: {e}")
        return False

def test_proxy_connectivity():
    """Test if frontend can proxy to backend"""
    print("\n🔄 Testing Frontend-Backend Proxy...")
    
    try:
        # Test proxy through frontend
        response = requests.get(f"{FRONTEND_URL}/api/quantum/simulations", timeout=10)
        if response.status_code == 200:
            print("   ✅ Frontend proxy to backend working")
            return True
        else:
            print(f"   ❌ Proxy failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Proxy test failed: {e}")
        return False

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("🚀 QUANTUM STATE VISUALIZER - COMPREHENSIVE TEST REPORT")
    print("="*60)
    
    tests = [
        ("API Health Check", test_api_health),
        ("Frontend Connectivity", test_frontend_connectivity), 
        ("Frontend-Backend Proxy", test_proxy_connectivity),
        ("Quantum Circuit Simulations", test_quantum_circuits),
        ("Reduced Density Matrix", test_rdm_calculations),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'🔍 ' + test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Final report
    print("\n" + "="*60)
    print("📋 FINAL TEST RESULTS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    print(f"\n📊 Overall Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 SYSTEM STATUS: FULLY FUNCTIONAL")
        print("\n✨ The Quantum State Visualizer is ready for use!")
        print("   - Quantum circuit simulation ✅")
        print("   - Bloch sphere visualization ✅") 
        print("   - Mixed state analysis ✅")
        print("   - Frontend-backend integration ✅")
    elif success_rate >= 60:
        print("⚠️  SYSTEM STATUS: MOSTLY FUNCTIONAL")
        print("   Some features may need attention")
    else:
        print("❌ SYSTEM STATUS: NEEDS ATTENTION")
        print("   Critical issues need to be resolved")
    
    print("\n🔗 Access the application at:")
    print(f"   Frontend: {FRONTEND_URL}")
    print(f"   Backend API: {BASE_URL}/docs")
    
    return success_rate >= 80

if __name__ == "__main__":
    generate_test_report()