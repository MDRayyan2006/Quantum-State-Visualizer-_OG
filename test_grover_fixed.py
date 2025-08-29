#!/usr/bin/env python3
"""
Test Grover's Algorithm Implementation
"""

import requests
import json

def test_grover_algorithm():
    """Test Grover's search algorithm with various configurations"""
    BASE_URL = "http://localhost:8004"
    
    test_cases = [
        {
            "name": "Basic 2-qubit test",
            "data": {"n_qubits": 2, "marked_state": "11", "iterations": 1}
        },
        {
            "name": "Standard 3-qubit test",
            "data": {"n_qubits": 3, "marked_state": "101", "iterations": 1}
        },
        {
            "name": "4-qubit test",
            "data": {"n_qubits": 4, "marked_state": "1010", "iterations": 2}
        }
    ]
    
    print("🔍 Testing Grover's Search Algorithm")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   Parameters: {test_case['data']}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/algorithms/grover", 
                                   json=test_case['data'], 
                                   timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   📊 Success Probability: {result['success_probability']:.4f} ({result['success_probability']*100:.2f}%)")
                print(f"   🎯 Target State: {result['marked_state']}")
                print(f"   🔄 Iterations: {result['iterations']}")
                
                # Check if target state has reasonable probability
                if result['success_probability'] > 0.1:  # At least 10% success
                    print(f"   ✅ Good success probability!")
                else:
                    print(f"   ⚠️  Low success probability - might need more iterations")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Details: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error: Backend not running on {BASE_URL}")
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout: Request took too long")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

    print(f"\n" + "=" * 50)
    print("🏁 Grover's algorithm testing completed!")

if __name__ == "__main__":
    test_grover_algorithm()