#!/usr/bin/env python3
"""
Test script to verify VQE parameter-dependent updates
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_vqe_parameter_updates():
    """Test that VQE energy and circuit update when parameters change"""
    print("🧪 Testing VQE Parameter-Dependent Updates")
    print("=" * 50)
    
    # Test different parameter combinations
    test_cases = [
        {
            "name": "H2 + sto-3g + COBYLA + 50 iterations",
            "params": {
                "molecule": "H2",
                "basis": "sto-3g", 
                "optimizer": "COBYLA",
                "max_iterations": 50
            }
        },
        {
            "name": "H2 + 6-31g + SPSA + 100 iterations",
            "params": {
                "molecule": "H2",
                "basis": "6-31g",
                "optimizer": "SPSA", 
                "max_iterations": 100
            }
        },
        {
            "name": "LiH + sto-3g + COBYLA + 75 iterations",
            "params": {
                "molecule": "LiH",
                "basis": "sto-3g",
                "optimizer": "COBYLA",
                "max_iterations": 75
            }
        },
        {
            "name": "BeH2 + 6-31g + SPSA + 100 iterations",
            "params": {
                "molecule": "BeH2",
                "basis": "6-31g",
                "optimizer": "SPSA",
                "max_iterations": 100
            }
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 Test {i}: {test_case['name']}")
        print(f"   Parameters: {test_case['params']}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/algorithms/vqe", 
                                   json=test_case['params'])
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract key information
                energy = result.get('energy', 0)
                optimal_params = result.get('optimal_parameters', [])
                gates = result.get('gates', [])
                circuit_length = len(result.get('circuit', ''))
                
                # Find RY gates with parameters
                ry_gates = [g for g in gates if g.get('type') == 'RY']
                
                print(f"   ✅ Energy: {energy:.6f}")
                print(f"   🔧 Optimal parameters: {optimal_params}")
                print(f"   🚪 Total gates: {len(gates)}")
                print(f"   📊 Circuit length: {circuit_length} chars")
                print(f"   🔄 RY gates: {len(ry_gates)}")
                
                if ry_gates:
                    for j, ry_gate in enumerate(ry_gates):
                        print(f"      RY[{j}]: parameter = {ry_gate.get('parameter', 'N/A')}")
                
                results.append({
                    'test_name': test_case['name'],
                    'params': test_case['params'],
                    'energy': energy,
                    'optimal_parameters': optimal_params,
                    'num_gates': len(gates),
                    'ry_parameters': [g.get('parameter') for g in ry_gates],
                    'circuit_length': circuit_length
                })
                
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Analysis
    print(f"\n📊 Analysis of {len(results)} test results:")
    print("=" * 50)
    
    if len(results) >= 2:
        # Check if energies are different
        energies = [r['energy'] for r in results]
        unique_energies = len(set(energies))
        print(f"🔍 Unique energy values: {unique_energies}/{len(results)}")
        
        # Check if parameters are different
        all_params = []
        for r in results:
            if r['optimal_parameters']:
                all_params.extend(r['optimal_parameters'])
        unique_params = len(set(all_params))
        print(f"🔧 Unique parameter values: {unique_params}")
        
        # Check if RY gate parameters are different
        all_ry_params = []
        for r in results:
            all_ry_params.extend(r['ry_parameters'])
        unique_ry_params = len(set(all_ry_params))
        print(f"🔄 Unique RY parameters: {unique_ry_params}")
        
        print(f"\n📈 Parameter Dependencies:")
        for i, result in enumerate(results):
            molecule = result['params']['molecule']
            basis = result['params']['basis'] 
            optimizer = result['params']['optimizer']
            iterations = result['params']['max_iterations']
            energy = result['energy']
            param = result['optimal_parameters'][0] if result['optimal_parameters'] else 'N/A'
            
            print(f"   {molecule} | {basis} | {optimizer} | {iterations:3d}it → "
                  f"E={energy:.6f}, θ={param}")
        
        # Verify parameter dependency
        if unique_energies > 1 and unique_params > 1:
            print(f"\n✅ SUCCESS: VQE parameters ARE updating correctly!")
            print(f"   - Found {unique_energies} different energy values")
            print(f"   - Found {unique_params} different parameter values")
        else:
            print(f"\n❌ FAILURE: VQE parameters are NOT updating correctly!")
            print(f"   - Energy variation: {unique_energies}/{len(results)}")
            print(f"   - Parameter variation: {unique_params}")
    
    return results

if __name__ == "__main__":
    try:
        results = test_vqe_parameter_updates()
        print(f"\n🎯 Test completed with {len(results)} successful runs")
    except Exception as e:
        print(f"❌ Test failed: {e}")