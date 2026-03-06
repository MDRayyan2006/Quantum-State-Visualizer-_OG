#!/usr/bin/env python3
"""
Minimal QAOA Testing Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import numpy as np
import uuid
import json

# Try importing qiskit components one by one
try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    print("✅ Qiskit imports successful")
except ImportError as e:
    print(f"❌ Qiskit import failed: {e}")
    # Create mock classes for testing
    class QuantumCircuit:
        def __init__(self, n_qubits, n_cbits):
            self.num_qubits = n_qubits
            self.num_clbits = n_cbits
            
        def h(self, qubit):
            pass
            
        def cx(self, control, target):
            pass
            
        def rz(self, angle, qubit):
            pass
            
        def rx(self, angle, qubit):
            pass
            
        def measure_all(self):
            pass
            
        def __str__(self):
            return f"QuantumCircuit({self.num_qubits} qubits, {self.num_clbits} classical bits)"
    
    class AerSimulator:
        def run(self, circuit, shots=1000):
            # Mock simulation results
            class MockResult:
                def result(self):
                    return self
                    
                def get_counts(self):
                    # Return mock measurement counts
                    if hasattr(circuit, 'num_qubits'):
                        n_qubits = circuit.num_qubits
                    else:
                        n_qubits = 2
                    
                    # Generate realistic looking counts
                    counts = {}
                    for i in range(min(4, 2**n_qubits)):  # Limit to avoid too many states
                        state = format(i, f'0{n_qubits}b')
                        count = np.random.randint(50, 300)
                        counts[state] = count
                    return counts
            
            return MockResult()
    
    print("🔄 Using mock Qiskit classes for testing")

app = FastAPI(title="QAOA Test Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for algorithm results
algorithm_results = {}

class QAOAMaxCutRequest(BaseModel):
    graph: List[List[int]]  # Adjacency list
    p_layers: int = 2
    optimizer: str = "COBYLA"
    max_iterations: int = 100

class QAOAResponse(BaseModel):
    id: str
    optimal_cost: float
    optimal_parameters: List[float]
    iterations: List[Dict]
    circuit: str
    cut_value: int
    # Additional debugging information
    graph_info: Optional[Dict] = None
    total_edges: Optional[int] = None
    convergence_data: Optional[Dict] = None

def create_maxcut_qaoa_circuit_with_params(graph: List[List[int]], p: int, gamma_params: List[float], beta_params: List[float]):
    """Create QAOA circuit with specific parameter values"""
    n_qubits = len(graph)
    circuit = QuantumCircuit(n_qubits, n_qubits)
    
    # Initial state: equal superposition
    circuit.h(range(n_qubits))
    
    # QAOA layers with specific parameters
    for layer in range(p):
        # Cost Hamiltonian (phase separator)
        gamma = gamma_params[layer]
        for i in range(n_qubits):
            for j in graph[i]:
                if j > i:  # Avoid double counting
                    circuit.cx(i, j)
                    circuit.rz(gamma, j)
                    circuit.cx(i, j)
        
        # Mixing Hamiltonian
        beta = beta_params[layer]
        for i in range(n_qubits):
            circuit.rx(beta, i)
    
    circuit.measure_all()
    return circuit

def calculate_maxcut_value(counts: dict, graph: List[List[int]]) -> int:
    """Calculate the MaxCut value from measurement counts"""
    n_qubits = len(graph)
    total_shots = sum(counts.values())
    weighted_cut_value = 0
    
    for bitstring, count in counts.items():
        # Extract the quantum register part (before any space)
        measured_state = bitstring.split()[0] if ' ' in bitstring else bitstring
        
        # Ensure bitstring has correct length
        if len(measured_state) != n_qubits:
            continue
            
        # Calculate cut value for this bitstring
        cut_value = 0
        for i in range(n_qubits):
            for j in graph[i]:  # j is a neighbor of vertex i
                if j > i:  # Avoid double counting edges
                    # Edge (i,j) is cut if vertices are in different sets
                    if measured_state[i] != measured_state[j]:
                        cut_value += 1
        
        # Weight by measurement frequency
        weighted_cut_value += cut_value * count
    
    # Return average cut value
    average_cut = weighted_cut_value / total_shots if total_shots > 0 else 0
    return int(round(average_cut))

@app.get("/")
async def root():
    return {
        "message": "QAOA Test Backend Running", 
        "status": "healthy",
        "endpoints": ["/api/algorithms/qaoa"]
    }

@app.post("/api/algorithms/qaoa", response_model=QAOAResponse)
async def run_qaoa(request: QAOAMaxCutRequest):
    """Run QAOA for MaxCut problem with enhanced debugging and detailed results"""
    try:
        # Validate graph input
        if not request.graph or len(request.graph) < 2:
            raise HTTPException(status_code=400, detail="Graph must have at least 2 nodes")
        
        n_qubits = len(request.graph)
        print(f"\\n🎯 Starting QAOA for MaxCut problem:")
        print(f"   📊 Graph size: {n_qubits} qubits")
        print(f"   🔄 QAOA layers (p): {request.p_layers}")
        print(f"   🔢 Max iterations: {request.max_iterations}")
        
        # Count edges and analyze graph structure
        total_edges = 0
        edge_list = []
        for i in range(n_qubits):
            for j in request.graph[i]:
                if j > i:  # Avoid double counting
                    total_edges += 1
                    edge_list.append((i, j))
        
        print(f"   🔗 Total edges: {total_edges}")
        print(f"   📋 Edge list: {edge_list}")
        
        # Calculate theoretical maximum cut for comparison
        max_possible_cut = total_edges  # In worst case, all edges could be cut
        
        # Enhanced optimization simulation
        iterations = []
        best_cost = float('inf')
        best_params = [0.0] * (2 * request.p_layers)
        best_cut_value = 0
        cost_history = []
        cut_history = []
        param_history = []
        
        print(f"\\n🔄 Starting QAOA optimization iterations...")
        
        # Simulate parameter optimization with enhanced tracking
        for i in range(min(request.max_iterations, 25)):  # Increased limit for better analysis
            # Generate parameters - use better initialization strategy
            if i == 0:
                # First iteration: use parameters that should give good cuts
                gamma_params = np.array([np.pi/3] * request.p_layers)  # Slightly adjusted gamma
                beta_params = np.array([np.pi/4] * request.p_layers)   # Adjusted beta for better mixing
                print(f"   🚀 Iteration {i}: Using initial parameters (γ={np.pi/3:.3f}, β={np.pi/4:.3f})")
            elif i < 5:
                # First few iterations: use known good parameter ranges
                gamma_params = np.random.uniform(np.pi/6, np.pi/2, request.p_layers)
                beta_params = np.random.uniform(np.pi/8, np.pi/3, request.p_layers)
                print(f"   🎲 Iteration {i}: Using guided random parameters")
            else:
                # Later iterations: explore more broadly but with some bias toward good regions
                gamma_params = np.random.uniform(0, np.pi, request.p_layers)
                beta_params = np.random.uniform(0, np.pi/2, request.p_layers)
                print(f"   🌍 Iteration {i}: Exploring broader parameter space")
            
            params = np.concatenate([gamma_params, beta_params])
            
            # Create parameterized circuit for this iteration
            param_circuit = create_maxcut_qaoa_circuit_with_params(
                request.graph, request.p_layers, gamma_params.tolist(), beta_params.tolist()
            )
            
            # Execute circuit using Aer simulator with more shots for better statistics
            simulator = AerSimulator()
            job = simulator.run(param_circuit, shots=2000)  # Increased shots for better accuracy
            result = job.result()
            counts = result.get_counts()
            
            # Calculate cut value from measurement results
            cut_value = calculate_maxcut_value(counts, request.graph)
            cost = -cut_value  # QAOA minimizes cost, MaxCut maximizes cut
            
            # Calculate additional statistics
            total_shots = sum(counts.values())
            most_frequent_state = max(counts, key=counts.get) if counts else "00"
            most_frequent_probability = counts.get(most_frequent_state, 0) / total_shots if total_shots > 0 else 0
            
            # Store detailed iteration data
            iteration_data = {
                "iteration": i,
                "cost": float(cost),
                "cut_value": cut_value,
                "parameters": params.tolist(),
                "gamma_params": gamma_params.tolist(),
                "beta_params": beta_params.tolist(),
                "measurement_counts": dict(counts),
                "most_frequent_state": most_frequent_state,
                "most_frequent_probability": float(most_frequent_probability),
                "total_shots": total_shots,
                "cut_efficiency": float(cut_value / max_possible_cut) if max_possible_cut > 0 else 0.0
            }
            
            iterations.append(iteration_data)
            cost_history.append(cost)
            cut_history.append(cut_value)
            param_history.append(params.tolist())
            
            # Print detailed iteration results
            print(f"   📊 Iteration {i} results:")
            print(f"      💰 Cost: {cost:.4f}")
            print(f"      ✂️  Cut value: {cut_value}/{max_possible_cut} ({100*cut_value/max_possible_cut:.1f}%)")
            print(f"      🎯 Most frequent state: {most_frequent_state} ({100*most_frequent_probability:.1f}%)")
            print(f"      📈 Parameters: γ={gamma_params}, β={beta_params}")
            
            # Update best result
            if cost < best_cost:
                best_cost = float(cost)
                best_params = params.tolist()
                best_cut_value = cut_value
                print(f"      ⭐ New best result! Cut value: {best_cut_value}")
        
        print(f"\\n🏆 QAOA optimization completed!")
        print(f"   🥇 Best cut value: {best_cut_value}/{max_possible_cut} ({100*best_cut_value/max_possible_cut:.1f}%)")
        print(f"   💰 Best cost: {best_cost:.4f}")
        
        # Calculate convergence metrics
        convergence_data = {
            "cost_history": cost_history,
            "cut_history": cut_history,
            "param_history": param_history,
            "improvement_iterations": [i for i, cost in enumerate(cost_history) if cost == min(cost_history[:i+1])],
            "final_improvement": abs(cost_history[0] - cost_history[-1]) if len(cost_history) > 1 else 0,
            "convergence_rate": sum(1 for i in range(1, len(cost_history)) if cost_history[i] < cost_history[i-1]) / len(cost_history) if len(cost_history) > 1 else 0
        }
        
        # Create final circuit with best parameters
        final_gamma = best_params[:request.p_layers]
        final_beta = best_params[request.p_layers:]
        final_circuit = create_maxcut_qaoa_circuit_with_params(
            request.graph, request.p_layers, final_gamma, final_beta
        )
        
        # Graph analysis information
        graph_info = {
            "nodes": n_qubits,
            "edges": total_edges,
            "edge_list": edge_list,
            "adjacency_list": request.graph,
            "max_possible_cut": max_possible_cut,
            "density": 2 * total_edges / (n_qubits * (n_qubits - 1)) if n_qubits > 1 else 0
        }
        
        # Generate unique ID
        result_id = str(uuid.uuid4())
        
        print(f"\\n💾 Storing results with ID: {result_id}")
        
        # Store enhanced results
        algorithm_results[result_id] = {
            "type": "qaoa",
            "optimal_cost": best_cost,
            "optimal_parameters": best_params,
            "iterations": iterations,
            "circuit": str(final_circuit),
            "cut_value": best_cut_value,
            "graph_info": graph_info,
            "total_edges": total_edges,
            "convergence_data": convergence_data
        }
        
        return QAOAResponse(
            id=result_id,
            optimal_cost=best_cost,
            optimal_parameters=best_params,
            iterations=iterations,
            circuit=str(final_circuit),
            cut_value=best_cut_value,
            graph_info=graph_info,
            total_edges=total_edges,
            convergence_data=convergence_data
        )
        
    except Exception as e:
        error_msg = f"QAOA execution failed: {str(e)}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting QAOA Test Backend on port 8004...")
    uvicorn.run(app, host="0.0.0.0", port=8004)