#!/usr/bin/env python3
"""
Test script to diagnose the quantum simulate API error
"""

import requests
import json

def test_simulate():
    BASE_URL = "http://localhost:8004"
    
    # Test simple circuit
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];"""

    data = {
        "qasm": qasm,
        "shots": 1000
    }

    try:
        print("🧪 Testing quantum simulate endpoint...")
        response = requests.post(f"{BASE_URL}/api/quantum/simulate", json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: ID={result['id']}, qubits={result['n_qubits']}")
            print(f"Statevector length: {len(result['statevector'])}")
            print(f"Measurement counts: {result['measurement_counts']}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the backend running on port 8004?")
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_simulate()