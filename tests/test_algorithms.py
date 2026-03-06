#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8002"

def test_grover_algorithm():
    """Test Grover's search algorithm"""
    print("Testing Grover's Search Algorithm...")
    
    grover_data = {
        "n_qubits": 3,
        "marked_state": "101",
        "iterations": 2
    }
    
    response = requests.post(f"{BASE_URL}/api/algorithms/grover", json=grover_data)
    print(f"Grover status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Algorithm ID: {result['id']}")
        print(f"Marked state: {result['marked_state']}")
        print(f"Success probability: {result['success_probability']:.4f}")
        print(f"Iterations: {result['iterations']}")
        print(f"Measurement counts: {result['measurement_counts']}")
        
        # Check if marked state has highest probability
        max_count = max(result['measurement_counts'].values())
        most_likely_state = [state for state, count in result['measurement_counts'].items() if count == max_count][0]
        print(f"Most likely measured state: {most_likely_state}")
        print(f"Target found: {most_likely_state == result['marked_state']}")
    else:
        print(f"Error: {response.text}")

def test_qft_algorithm():
    """Test Quantum Fourier Transform"""
    print("\nTesting Quantum Fourier Transform...")
    
    qft_data = {
        "n_qubits": 3,
        "input_state": "101"
    }
    
    response = requests.post(f"{BASE_URL}/api/algorithms/qft", json=qft_data)
    print(f"QFT status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Algorithm ID: {result['id']}")
        print(f"Input state: {result['input_state']}")
        print(f"Output state: {result['output_state']}")
        print(f"Fourier coefficients (first 4): {result['fourier_coefficients'][:4]}")
    else:
        print(f"Error: {response.text}")

def test_teleportation():
    """Test Quantum Teleportation"""
    print("\nTesting Quantum Teleportation...")
    
    teleport_data = {
        "message_state": "+"
    }
    
    response = requests.post(f"{BASE_URL}/api/algorithms/teleport", json=teleport_data)
    print(f"Teleportation status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Algorithm ID: {result['id']}")
        print(f"Message state: {result['message_state']}")
        print(f"Teleported state: {result['teleported_state']}")
        print(f"Fidelity: {result['fidelity']:.4f}")
    else:
        print(f"Error: {response.text}")

def test_vqe_algorithm():
    """Test Variational Quantum Eigensolver"""
    print("\nTesting VQE Algorithm...")
    
    vqe_data = {
        "molecule": "H2",
        "basis": "sto-3g",
        "optimizer": "COBYLA",
        "max_iterations": 10  # Keep it small for testing
    }
    
    response = requests.post(f"{BASE_URL}/api/algorithms/vqe", json=vqe_data)
    print(f"VQE status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Algorithm ID: {result['id']}")
        print(f"Ground state energy: {result['energy']:.6f}")
        print(f"Optimal parameters: {result['optimal_parameters']}")
        print(f"Convergence iterations: {len(result['iterations'])}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Testing Quantum Algorithms")
    print("=" * 50)
    
    try:
        test_grover_algorithm()
        test_qft_algorithm()
        test_teleportation()
        test_vqe_algorithm()
        print("\n" + "=" * 50)
        print("Algorithm testing completed!")
    except Exception as e:
        print(f"Test failed with error: {e}")