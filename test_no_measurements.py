#!/usr/bin/env python3
"""
Test the specific circuit without measurements that's causing the error
"""

import requests
import json

def test_no_measurements():
    BASE_URL = "http://localhost:8004"
    
    print("🧪 Testing circuit without measurements")
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];"""

    data = {"qasm": qasm, "shots": 1000}
    
    try:
        response = requests.post(f"{BASE_URL}/api/quantum/simulate", json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: ID={result['id']}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_no_measurements()