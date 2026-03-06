#!/usr/bin/env python3
"""
Test the new API
"""

import requests
import json

def test_new_api():
    print("🧪 Testing New API")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8004/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test simulation endpoint
    test_qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];
    measure q[0] -> c[0];
    measure q[1] -> c[1];
    """
    
    data = {
        "qasm": test_qasm,
        "shots": 1000,
        "backend": "aer_simulator"
    }
    
    try:
        response = requests.post(
            "http://localhost:8004/api/quantum/simulate",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Simulation test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_new_api()
