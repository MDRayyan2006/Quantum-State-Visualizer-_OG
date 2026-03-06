#!/usr/bin/env python3
import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_quantum_simulation():
    """Test quantum simulation endpoint"""
    # Simple Bell state circuit
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    data = {
        "qasm": qasm,
        "shots": 1000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/quantum/simulate", json=data)
        print(f"\nQuantum simulation: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"ID: {result['id']}")
            print(f"Qubits: {result['n_qubits']}")
            print(f"Statevector: {result['statevector'][:4]}...")  # First 4 elements
            print(f"Probabilities: {result['probabilities']}")
            print(f"Measurement counts: {result['measurement_counts']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_health()
    test_quantum_simulation()