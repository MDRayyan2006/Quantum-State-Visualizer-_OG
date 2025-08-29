import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from dash_bootstrap_components import themes
import dash_bootstrap_components as dbc

def create_dash_app():
    """Create and configure the Dash app for quantum analytics"""
    
    # Create Dash app with proper configuration for iframe embedding
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            themes.BOOTSTRAP,
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
        ],
        url_base_pathname='/',
        suppress_callback_exceptions=True,
        update_title=None,  # Prevent title updates that can cause issues in iframes
        serve_locally=True  # Serve assets locally to avoid CORS issues
    )
    
    # Configure for iframe embedding
    app.config.suppress_callback_exceptions = True
    
    # Add custom CSS for iframe compatibility
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                body {
                    margin: 0;
                    padding: 10px;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .dash-loading {
                    display: none;
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    
    # App layout with dynamic algorithm-specific graphs
    app.layout = dbc.Container([
        # Header section
        dbc.Row([
            dbc.Col([
                html.H1("🚀 Quantum Analytics Dashboard", 
                        className="text-center text-primary mb-4"),
                html.P("Dynamic algorithm analysis and performance metrics",
                       className="text-center text-muted")
            ])
        ]),
        
        # Algorithm Results Detection
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔍 Latest Algorithm Results"),
                    dbc.CardBody([
                        html.Div(id='algorithm-status'),
                        dbc.Button("Refresh Results", id="refresh-btn", 
                                  color="primary", className="mt-2")
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Dynamic Algorithm-Specific Graphs
        html.Div(id='dynamic-graphs-container'),
        
        # Traditional Analysis Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Interactive Analysis"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='analysis-type',
                            options=[
                                {'label': 'Algorithm Convergence', 'value': 'convergence'},
                                {'label': 'Parameter Evolution', 'value': 'parameters'},
                                {'label': 'Energy Landscapes', 'value': 'energy'},
                                {'label': 'Success Probability', 'value': 'probability'}
                            ],
                            value='convergence',
                            className="mb-3"
                        ),
                        dcc.Graph(id='interactive-plot')
                    ])
                ])
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("⚙️ Controls"),
                    dbc.CardBody([
                        html.Label("Analysis Depth:"),
                        dcc.Slider(
                            id='analysis-depth',
                            min=1, max=10, step=1, value=5,
                            marks={i: str(i) for i in range(1, 11)},
                            className="mb-3"
                        ),
                        
                        html.Label("Smoothing:"),
                        dcc.Slider(
                            id='smoothing',
                            min=0, max=1, step=0.1, value=0.3,
                            marks={0: '0', 0.5: '0.5', 1: '1'},
                            className="mb-3"
                        ),
                        
                        dbc.Button("Export Data", id="export-btn", 
                                  color="success", className="w-100")
                    ])
                ])
            ], width=4)
        ])
        
    ], fluid=True, className="py-4")
    
    # Import requests for API calls
    import requests
    
    # Callback for algorithm status and refresh
    @app.callback(
        Output('algorithm-status', 'children'),
        [Input('refresh-btn', 'n_clicks')],
        prevent_initial_call=False
    )
    def update_algorithm_status(n_clicks):
        try:
            # Fetch latest algorithm results from the API
            response = requests.get('http://localhost:8000/api/algorithms/results/latest')
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    result = data['data']
                    algorithm_type = result.get('type', 'Unknown').upper()
                    
                    # Create status display based on algorithm type
                    if algorithm_type == 'VQE':
                        energy = result.get('energy', 0)
                        molecule = result.get('molecule', 'Unknown')
                        return dbc.Alert([
                            html.H5(f"⚙️ VQE Results - {molecule}", className="mb-2"),
                            html.P(f"Ground State Energy: {energy:.6f} Ha"),
                            html.P(f"Parameters: {result.get('optimal_parameters', [])}"),
                            html.Small(f"Last updated: Just now", className="text-muted")
                        ], color="success")
                    
                    elif algorithm_type == 'GROVER':
                        prob = result.get('success_probability', 0)
                        marked = result.get('marked_state', 'Unknown')
                        return dbc.Alert([
                            html.H5(f"🔍 Grover's Algorithm", className="mb-2"),
                            html.P(f"Success Probability: {prob*100:.2f}%"),
                            html.P(f"Marked State: |{marked}⟩"),
                            html.Small(f"Last updated: Just now", className="text-muted")
                        ], color="info")
                    
                    elif algorithm_type == 'QFT':
                        input_state = result.get('input_state', 'Unknown')
                        return dbc.Alert([
                            html.H5(f"🌀 Quantum Fourier Transform", className="mb-2"),
                            html.P(f"Input State: {input_state}"),
                            html.P(f"Qubits: {result.get('n_qubits', 'Unknown')}"),
                            html.Small(f"Last updated: Just now", className="text-muted")
                        ], color="warning")
                    
                    elif algorithm_type == 'TELEPORTATION':
                        fidelity = result.get('fidelity', 0)
                        message = result.get('message_state', 'Unknown')
                        return dbc.Alert([
                            html.H5(f"📡 Quantum Teleportation", className="mb-2"),
                            html.P(f"Fidelity: {fidelity*100:.2f}%"),
                            html.P(f"Message State: |{message}⟩"),
                            html.Small(f"Last updated: Just now", className="text-muted")
                        ], color="primary")
                    
                    else:
                        return dbc.Alert([
                            html.H5(f"🔬 {algorithm_type} Results", className="mb-2"),
                            html.P("Algorithm executed successfully"),
                            html.Small(f"Last updated: Just now", className="text-muted")
                        ], color="secondary")
                
                else:
                    return dbc.Alert("No algorithm results available. Run an algorithm first.", color="light")
            else:
                return dbc.Alert("Could not fetch algorithm results.", color="danger")
        except Exception as e:
            return dbc.Alert(f"Error: {str(e)}", color="danger")
    
    # Callback for dynamic graphs container
    @app.callback(
        Output('dynamic-graphs-container', 'children'),
        [Input('refresh-btn', 'n_clicks')],
        prevent_initial_call=False
    )
    def update_dynamic_graphs(n_clicks):
        try:
            # Fetch latest algorithm results
            response = requests.get('http://localhost:8000/api/algorithms/results/latest')
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    result = data['data']
                    algorithm_type = result.get('type', 'unknown')
                    
                    # Create algorithm-specific graphs
                    if algorithm_type == 'vqe':
                        return create_vqe_graphs(result)
                    elif algorithm_type == 'grover':
                        return create_grover_graphs(result)
                    elif algorithm_type == 'qft':
                        return create_qft_graphs(result)
                    elif algorithm_type == 'teleportation':
                        return create_teleportation_graphs(result)
                    else:
                        return create_generic_graphs(result)
                else:
                    return html.Div([
                        dbc.Alert("No algorithm data available for visualization.", color="info")
                    ])
            else:
                return html.Div([
                    dbc.Alert("Could not fetch algorithm results for visualization.", color="warning")
                ])
        except Exception as e:
            return html.Div([
                dbc.Alert(f"Error creating dynamic graphs: {str(e)}", color="danger")
            ])
    
    # Callback for interactive plot
    @app.callback(
        Output('interactive-plot', 'figure'),
        [Input('analysis-type', 'value'),
         Input('analysis-depth', 'value'),
         Input('smoothing', 'value')],
        prevent_initial_call=False
    )
    def update_interactive_plot(analysis_type, depth, smoothing):
        try:
            # Fetch latest algorithm results for context
            response = requests.get('http://localhost:8000/api/algorithms/results/latest')
            if response.status_code == 200:
                data = response.json()
                result_data = data.get('data')
            else:
                result_data = None
            
            if analysis_type == 'convergence':
                return create_convergence_analysis(result_data, depth, smoothing)
            elif analysis_type == 'parameters':
                return create_parameter_evolution(result_data, depth, smoothing)
            elif analysis_type == 'energy':
                return create_energy_landscape(result_data, depth, smoothing)
            elif analysis_type == 'probability':
                return create_probability_analysis(result_data, depth, smoothing)
            else:
                return go.Figure().add_annotation(
                    text="Select an analysis type",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
        except Exception as e:
            return go.Figure().add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    return app

def create_vqe_graphs(result_data):
    """Create VQE-specific visualization graphs with enhanced aesthetics"""
    try:
        iterations = result_data.get('iterations', [])
        energy = result_data.get('energy', 0)
        params = result_data.get('optimal_parameters', [])
        molecule = result_data.get('molecule', 'Unknown')
        basis = result_data.get('basis', 'Unknown')
        optimizer = result_data.get('optimizer', 'Unknown')
        
        graphs = []
        
        # 1. Energy Convergence Plot with enhanced styling
        if iterations and len(iterations) > 0:
            iters = [item['iteration'] for item in iterations]
            energies = [item['energy'] for item in iterations]
            
            energy_fig = go.Figure()
            
            # Main convergence line
            energy_fig.add_trace(go.Scatter(
                x=iters, 
                y=energies,
                mode='lines+markers',
                name='Energy Convergence',
                line=dict(color='#00FF88', width=3, shape='spline'),
                marker=dict(size=8, color='#00FF88', line=dict(width=2, color='white')),
                fill='tonexty' if len(energies) > 1 else None,
                fillcolor='rgba(0, 255, 136, 0.1)'
            ))
            
            # Add target line if available
            if len(energies) > 1:
                target_energy = min(energies)
                energy_fig.add_hline(
                    y=target_energy, 
                    line_dash="dash", 
                    line_color="#FF6B6B",
                    annotation_text=f"Ground State: {target_energy:.6f} Ha"
                )
            
            energy_fig.update_layout(
                title=dict(
                    text=f"🎯 VQE Energy Convergence - {molecule} ({basis}, {optimizer})",
                    font=dict(size=18, color='white')
                ),
                xaxis_title="Iteration",
                yaxis_title="Energy (Hartree)",
                template="plotly_dark",
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            graphs.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("⚡ Energy Convergence Analysis", className="bg-success text-white"),
                        dbc.CardBody([dcc.Graph(figure=energy_fig, config={'displayModeBar': False})])
                    ])
                ], width=6)
            )
        
        # 2. Parameter Evolution with enhanced styling
        if iterations and len(iterations) > 0 and all('parameters' in item for item in iterations):
            param_fig = go.Figure()
            
            # Extract parameter evolution
            for param_idx in range(len(iterations[0]['parameters'])):
                param_values = [item['parameters'][param_idx] for item in iterations]
                
                param_fig.add_trace(go.Scatter(
                    x=iters,
                    y=param_values,
                    mode='lines+markers',
                    name=f'θ{param_idx + 1}',
                    line=dict(width=3),
                    marker=dict(size=6)
                ))
            
            param_fig.update_layout(
                title=dict(
                    text="🔧 Parameter Evolution",
                    font=dict(size=18, color='white')
                ),
                xaxis_title="Iteration",
                yaxis_title="Parameter Value",
                template="plotly_dark",
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            graphs.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("🎛️ Parameter Optimization", className="bg-info text-white"),
                        dbc.CardBody([dcc.Graph(figure=param_fig, config={'displayModeBar': False})])
                    ])
                ], width=6)
            )
        
        # 3. Energy Landscape Visualization
        if params and len(params) > 0:
            # Create parameter space around optimal point
            param_range = np.linspace(params[0] - 0.5, params[0] + 0.5, 50)
            energy_landscape = []
            
            for p in param_range:
                # Mock energy landscape calculation
                mock_energy = energy + 0.1 * (p - params[0])**2 + 0.02 * np.sin(10 * p)
                energy_landscape.append(mock_energy)
            
            landscape_fig = go.Figure()
            
            # Energy landscape
            landscape_fig.add_trace(go.Scatter(
                x=param_range,
                y=energy_landscape,
                mode='lines',
                name='Energy Landscape',
                line=dict(color='#FF6B6B', width=3),
                fill='tonexty',
                fillcolor='rgba(255, 107, 107, 0.2)'
            ))
            
            # Mark optimal point
            landscape_fig.add_trace(go.Scatter(
                x=[params[0]],
                y=[energy],
                mode='markers',
                name='Optimal Point',
                marker=dict(size=15, color='#FFD93D', symbol='star', line=dict(width=2, color='white'))
            ))
            
            landscape_fig.update_layout(
                title=dict(
                    text="🏔️ Energy Landscape",
                    font=dict(size=18, color='white')
                ),
                xaxis_title="Parameter Value",
                yaxis_title="Energy (Hartree)",
                template="plotly_dark",
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            graphs.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("⛰️ Parameter Landscape", className="bg-warning text-dark"),
                        dbc.CardBody([dcc.Graph(figure=landscape_fig, config={'displayModeBar': False})])
                    ])
                ], width=12)
            )
        
        # 4. Molecular Properties Summary
        molecule_data = {
            'H2': {'bond_length': 0.74, 'exact_energy': -1.8572, 'electrons': 2},
            'LiH': {'bond_length': 1.60, 'exact_energy': -8.9472, 'electrons': 4},
            'BeH2': {'bond_length': 1.34, 'exact_energy': -15.2372, 'electrons': 6}
        }
        
        mol_info = molecule_data.get(molecule, {'bond_length': 'Unknown', 'exact_energy': 'Unknown', 'electrons': 'Unknown'})
        error = abs(energy - mol_info['exact_energy']) if isinstance(mol_info['exact_energy'], (int, float)) else 'Unknown'
        
        summary_card = dbc.Col([
            dbc.Card([
                dbc.CardHeader(f"📊 {molecule} Molecular Summary", className="bg-primary text-white"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Computed Energy", className="text-muted"),
                            html.H4(f"{energy:.6f} Ha", className="text-success")
                        ], width=4),
                        dbc.Col([
                            html.H6("Chemical Error", className="text-muted"),
                            html.H4(f"{error:.6f} Ha" if isinstance(error, (int, float)) else "Unknown", 
                                   className="text-warning" if isinstance(error, (int, float)) and error < 0.01 else "text-danger")
                        ], width=4),
                        dbc.Col([
                            html.H6("Optimal Parameter", className="text-muted"),
                            html.H4(f"{params[0]:.5f}" if params else "N/A", className="text-info")
                        ], width=4)
                    ]),
                    html.Hr(),
                    html.P(f"Basis Set: {basis} | Optimizer: {optimizer} | Electrons: {mol_info['electrons']}", 
                          className="text-muted mb-0")
                ])
            ])
        ], width=12)
        
        graphs.append(summary_card)
        
        # Return all graphs in a responsive layout
        return dbc.Row(graphs, className="g-4")
        
    except Exception as e:
        return dbc.Alert(f"Error creating VQE graphs: {str(e)}", color="danger")

def create_grover_graphs(result_data):
    """Create Grover's algorithm specific visualization graphs"""
    try:
        success_prob = result_data.get('success_probability', 0)
        marked_state = result_data.get('marked_state', 'Unknown')
        n_qubits = result_data.get('n_qubits', 3)
        counts = result_data.get('measurement_counts', {})
        
        # Success probability visualization
        prob_fig = go.Figure(data=[
            go.Bar(
                x=['Success', 'Other States'],
                y=[success_prob, 1 - success_prob],
                marker_color=['#2ECC71', '#E74C3C']
            )
        ])
        prob_fig.update_layout(
            title=f"Grover Search Success Probability - |{marked_state}⟩",
            yaxis_title="Probability",
            template="plotly_dark",
            height=400
        )
        
        # Measurement counts histogram
        if counts:
            states = list(counts.keys())
            counts_vals = list(counts.values())
            
            counts_fig = go.Figure(data=[
                go.Bar(
                    x=[f"|{state}⟩" for state in states],
                    y=counts_vals,
                    marker_color=['#2ECC71' if state == marked_state else '#3498DB' for state in states]
                )
            ])
            counts_fig.update_layout(
                title="Measurement Results Distribution",
                xaxis_title="Quantum States",
                yaxis_title="Count",
                template="plotly_dark",
                height=400
            )
        else:
            counts_fig = go.Figure().add_annotation(
                text="No measurement data available",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎯 Success Probability"),
                    dbc.CardBody([dcc.Graph(figure=prob_fig)])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Measurement Counts"),
                    dbc.CardBody([dcc.Graph(figure=counts_fig)])
                ])
            ], width=6)
        ], className="mb-4")
        
    except Exception as e:
        return dbc.Alert(f"Error creating Grover graphs: {str(e)}", color="danger")

def create_qft_graphs(result_data):
    """Create QFT-specific visualization graphs"""
    try:
        input_state = result_data.get('input_state', 'Unknown')
        output_state = result_data.get('output_state', 'Unknown')
        n_qubits = result_data.get('n_qubits', 4)
        fourier_coeffs = result_data.get('fourier_coefficients', [])
        
        # Fourier coefficients visualization
        if fourier_coeffs:
            # Parse complex numbers from strings
            coeffs_real = []
            coeffs_imag = []
            for coeff_str in fourier_coeffs[:8]:  # Limit to first 8
                try:
                    coeff = complex(coeff_str.replace('i', 'j'))  # Python uses j for imaginary
                    coeffs_real.append(coeff.real)
                    coeffs_imag.append(coeff.imag)
                except:
                    coeffs_real.append(0)
                    coeffs_imag.append(0)
            
            fourier_fig = go.Figure()
            fourier_fig.add_trace(go.Bar(
                name='Real Part',
                x=[f'k={i}' for i in range(len(coeffs_real))],
                y=coeffs_real,
                marker_color='#4F82FF'
            ))
            fourier_fig.add_trace(go.Bar(
                name='Imaginary Part',
                x=[f'k={i}' for i in range(len(coeffs_imag))],
                y=coeffs_imag,
                marker_color='#F39C12'
            ))
            
            fourier_fig.update_layout(
                title="Fourier Coefficients",
                xaxis_title="Frequency",
                yaxis_title="Amplitude",
                barmode='group',
                template="plotly_dark",
                height=400
            )
        else:
            fourier_fig = go.Figure().add_annotation(
                text="No Fourier coefficient data available",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        # State transformation visualization
        state_fig = go.Figure()
        state_fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[1, 1],
            mode='markers+text',
            text=[f'Input: {input_state}', f'Output: {output_state}'],
            textposition='top center',
            marker=dict(size=20, color=['#2ECC71', '#E74C3C'])
        ))
        state_fig.update_layout(
            title="QFT State Transformation",
            showlegend=False,
            template="plotly_dark",
            height=400,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🌀 Fourier Transform"),
                    dbc.CardBody([dcc.Graph(figure=fourier_fig)])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔄 State Transformation"),
                    dbc.CardBody([dcc.Graph(figure=state_fig)])
                ])
            ], width=6)
        ], className="mb-4")
        
    except Exception as e:
        return dbc.Alert(f"Error creating QFT graphs: {str(e)}", color="danger")

def create_teleportation_graphs(result_data):
    """Create Teleportation-specific visualization graphs"""
    try:
        fidelity = result_data.get('fidelity', 0)
        message_state = result_data.get('message_state', 'Unknown')
        teleported_state = result_data.get('teleported_state', 'Unknown')
        
        # Fidelity visualization
        fidelity_fig = go.Figure()
        fidelity_fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=fidelity * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Teleportation Fidelity (%)"},
            delta={'reference': 95},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#2ECC71"},
                'steps': [
                    {'range': [0, 50], 'color': "#E74C3C"},
                    {'range': [50, 90], 'color': "#F39C12"},
                    {'range': [90, 100], 'color': "#2ECC71"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fidelity_fig.update_layout(
            template="plotly_dark",
            height=400
        )
        
        # State comparison
        state_fig = go.Figure()
        state_fig.add_trace(go.Bar(
            x=['Original', 'Teleported'],
            y=[1, fidelity],
            text=[f'|{message_state}⟩', f'|{teleported_state}⟩'],
            textposition='auto',
            marker_color=['#3498DB', '#2ECC71']
        ))
        state_fig.update_layout(
            title="State Comparison",
            yaxis_title="Fidelity",
            template="plotly_dark",
            height=400
        )
        
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎯 Teleportation Fidelity"),
                    dbc.CardBody([dcc.Graph(figure=fidelity_fig)])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔄 State Comparison"),
                    dbc.CardBody([dcc.Graph(figure=state_fig)])
                ])
            ], width=6)
        ], className="mb-4")
        
    except Exception as e:
        return dbc.Alert(f"Error creating Teleportation graphs: {str(e)}", color="danger")

def create_generic_graphs(result_data):
    """Create generic graphs for unknown algorithm types"""
    algorithm_type = result_data.get('type', 'Unknown').upper()
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(f"🔬 {algorithm_type} Results"),
                dbc.CardBody([
                    html.Pre(str(result_data)[:500] + "..." if len(str(result_data)) > 500 else str(result_data)),
                    dbc.Alert("Visualization for this algorithm type is not yet implemented.", color="info")
                ])
            ])
        ], width=12)
    ], className="mb-4")

def create_convergence_analysis(result_data, depth, smoothing):
    """Create convergence analysis plot"""
    if not result_data:
        return go.Figure().add_annotation(
            text="No algorithm data available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    algorithm_type = result_data.get('type', 'unknown')
    
    if algorithm_type == 'vqe':
        iterations = result_data.get('iterations', [])
        if iterations:
            x = [i['iteration'] for i in iterations]
            y = [i['energy'] for i in iterations]
            
            # Apply smoothing
            if smoothing > 0 and len(y) > 2:
                from scipy.signal import savgol_filter
                window_length = min(len(y), max(3, int(len(y) * smoothing)))
                if window_length % 2 == 0:
                    window_length += 1
                y_smooth = savgol_filter(y, window_length, 3)
            else:
                y_smooth = y
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Raw Data', opacity=0.6))
            fig.add_trace(go.Scatter(x=x, y=y_smooth, mode='lines', name='Smoothed', line=dict(width=3)))
            fig.update_layout(
                title="VQE Energy Convergence Analysis",
                xaxis_title="Iteration",
                yaxis_title="Energy (Ha)",
                template="plotly_dark"
            )
            return fig
    
    return go.Figure().add_annotation(
        text="Convergence analysis not available for this algorithm",
        xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
    )

def create_parameter_evolution(result_data, depth, smoothing):
    """Create parameter evolution plot"""
    if not result_data:
        return go.Figure().add_annotation(
            text="No algorithm data available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    algorithm_type = result_data.get('type', 'unknown')
    
    if algorithm_type == 'vqe':
        iterations = result_data.get('iterations', [])
        if iterations:
            x = [i['iteration'] for i in iterations]
            y = [i['parameters'][0] if i.get('parameters') else 0 for i in iterations]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='RY Parameter'))
            fig.update_layout(
                title="VQE Parameter Evolution",
                xaxis_title="Iteration",
                yaxis_title="Parameter Value",
                template="plotly_dark"
            )
            return fig
    
    return go.Figure().add_annotation(
        text="Parameter evolution not available for this algorithm",
        xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
    )

def create_energy_landscape(result_data, depth, smoothing):
    """Create energy landscape visualization"""
    # Generate mock energy landscape data
    x = np.linspace(-np.pi, np.pi, 50)
    y = np.linspace(-np.pi, np.pi, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y) + 0.5 * np.sin(2*X) + 0.3 * np.cos(3*Y)
    
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
    fig.update_layout(
        title="Energy Landscape (Mock Data)",
        scene=dict(
            xaxis_title="Parameter 1",
            yaxis_title="Parameter 2",
            zaxis_title="Energy"
        ),
        template="plotly_dark"
    )
    return fig

def create_probability_analysis(result_data, depth, smoothing):
    """Create probability analysis plot"""
    if not result_data:
        return go.Figure().add_annotation(
            text="No algorithm data available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    algorithm_type = result_data.get('type', 'unknown')
    
    if algorithm_type == 'grover':
        success_prob = result_data.get('success_probability', 0)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Success', 'Failure'],
            y=[success_prob, 1 - success_prob],
            marker_color=['#2ECC71', '#E74C3C']
        ))
        fig.update_layout(
            title="Grover Search Probability Analysis",
            yaxis_title="Probability",
            template="plotly_dark"
        )
        return fig
    
    return go.Figure().add_annotation(
        text="Probability analysis not available for this algorithm",
        xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
    )
    
    fig = go.Figure()
    
    for qubit in range(min(n_qubits, 4)):  # Limit to 4 qubits for visualization
        # Generate Bloch vector evolution with noise
        x = np.cos(time + qubit * np.pi/4) * (1 - noise_level * np.random.random(time_steps))
        y = np.sin(time + qubit * np.pi/4) * (1 - noise_level * np.random.random(time_steps))
        z = np.cos(2*time + qubit * np.pi/2) * (1 - noise_level * np.random.random(time_steps))
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines+markers',
            name=f'Qubit {qubit}',
            line=dict(width=3),
            marker=dict(size=4)
        ))
    
    # Add unit sphere
    phi = np.linspace(0, 2*np.pi, 20)
    theta = np.linspace(-np.pi/2, np.pi/2, 20)
    phi, theta = np.meshgrid(phi, theta)
    
    sphere_x = np.cos(theta) * np.cos(phi)
    sphere_y = np.cos(theta) * np.sin(phi)
    sphere_z = np.sin(theta)
    
    fig.add_trace(go.Surface(
        x=sphere_x, y=sphere_y, z=sphere_z,
        opacity=0.1,
        colorscale='Blues',
        showscale=False,
        name='Unit Sphere'
    ))
    
    fig.update_layout(
        title=f'Bloch Sphere Evolution (Noise: {noise_level:.2f})',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        height=500
    )
    
    return fig

def create_entanglement_plot(n_qubits, noise_level):
    """Create entanglement analysis plot"""
    if n_qubits < 2:
        return go.Figure().add_annotation(
            text="Need at least 2 qubits for entanglement analysis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Generate mock entanglement data
    qubit_pairs = [(i, j) for i in range(n_qubits) for j in range(i+1, n_qubits)]
    
    fig = go.Figure()
    
    for i, (q1, q2) in enumerate(qubit_pairs):
        # Mock entanglement entropy
        entropy = np.random.exponential(0.5) * (1 - noise_level)
        concurrence = np.random.random() * (1 - noise_level)
        
        fig.add_trace(go.Bar(
            x=[f'Q{q1}-Q{q2}'],
            y=[entropy],
            name=f'Entropy Q{q1}-Q{q2}',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            x=[f'Q{q1}-Q{q2}'],
            y=[concurrence],
            name=f'Concurrence Q{q1}-Q{q2}',
            marker_color='lightcoral'
        ))
    
    fig.update_layout(
        title=f'Entanglement Analysis (Noise: {noise_level:.2f})',
        xaxis_title='Qubit Pairs',
        yaxis_title='Value',
        barmode='group',
        height=400
    )
    
    return fig

def create_convergence_plot(n_qubits, noise_level):
    """Create algorithm convergence plot"""
    iterations = 100
    x = np.arange(iterations)
    
    # Mock convergence data for different algorithms
    vqe_energy = -1.137 + 0.1 * np.exp(-x/20) + noise_level * np.random.random(iterations)
    qaoa_cost = -5.0 + 2.0 * np.exp(-x/15) + noise_level * np.random.random(iterations)
    grover_prob = 0.25 + 0.75 * (1 - np.exp(-x/10)) + noise_level * np.random.random(iterations)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=vqe_energy,
        mode='lines+markers',
        name='VQE Energy',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=qaoa_cost,
        mode='lines+markers',
        name='QAOA Cost',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=grover_prob,
        mode='lines+markers',
        name='Grover Success Prob',
        line=dict(color='green', width=2)
    ))
    
    fig.update_layout(
        title=f'Algorithm Convergence (Noise: {noise_level:.2f})',
        xaxis_title='Iteration',
        yaxis_title='Value',
        height=400
    )
    
    return fig

def create_noise_analysis_plot(n_qubits, noise_level):
    """Create noise impact analysis plot"""
    noise_levels = np.linspace(0, 1, 20)
    
    # Mock fidelity and purity data
    fidelity = np.exp(-noise_levels * 2) + 0.1 * np.random.random(len(noise_levels))
    purity = np.exp(-noise_levels * 1.5) + 0.05 * np.random.random(len(noise_levels))
    entropy = 1 - np.exp(-noise_levels * 1.2) + 0.02 * np.random.random(len(noise_levels))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=noise_levels, y=fidelity,
        mode='lines+markers',
        name='Fidelity',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=noise_levels, y=purity,
        mode='lines+markers',
        name='Purity',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=noise_levels, y=entropy,
        mode='lines+markers',
        name='Entropy',
        line=dict(color='green', width=2)
    ))
    
    # Add vertical line for current noise level
    fig.add_vline(x=noise_level, line_dash="dash", line_color="orange")
    
    fig.update_layout(
        title='Noise Impact on Quantum State',
        xaxis_title='Noise Level',
        yaxis_title='Value',
        height=400
    )
    
    return fig

def create_algorithm_performance_plot(n_qubits, iterations):
    """Create algorithm performance comparison plot"""
    algorithms = ['VQE', 'QAOA', 'Grover', 'QFT', 'Teleport']
    
    # Mock performance metrics
    execution_time = [0.5 + n_qubits * 0.1, 0.3 + n_qubits * 0.15, 
                      0.2 + n_qubits * 0.05, 0.1 + n_qubits * 0.08, 0.15]
    success_rate = [0.85, 0.78, 0.92, 0.95, 0.88]
    resource_usage = [0.7 + n_qubits * 0.05, 0.6 + n_qubits * 0.08,
                      0.4 + n_qubits * 0.03, 0.3 + n_qubits * 0.06, 0.5]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=algorithms,
        y=execution_time,
        name='Execution Time (s)',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=algorithms,
        y=success_rate,
        name='Success Rate',
        marker_color='lightgreen'
    ))
    
    fig.add_trace(go.Bar(
        x=algorithms,
        y=resource_usage,
        name='Resource Usage',
        marker_color='lightcoral'
    ))
    
    fig.update_layout(
        title=f'Algorithm Performance Comparison ({n_qubits} qubits, {iterations} iterations)',
        xaxis_title='Algorithm',
        yaxis_title='Value',
        barmode='group',
        height=400
    )
    
    return fig

def create_quantum_network_plot(n_qubits):
    """Create quantum network visualization"""
    if n_qubits < 2:
        return go.Figure().add_annotation(
            text="Need at least 2 qubits for network visualization",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Create network layout
    nodes = []
    edges = []
    
    for i in range(n_qubits):
        # Position nodes in a circle
        angle = 2 * np.pi * i / n_qubits
        x = np.cos(angle)
        y = np.sin(angle)
        
        nodes.append(dict(
            x=x, y=y,
            text=f'Q{i}',
            mode='markers+text',
            marker=dict(size=20, color='lightblue'),
            textposition='middle center'
        ))
        
        # Add edges between adjacent qubits
        next_i = (i + 1) % n_qubits
        next_angle = 2 * np.pi * next_i / n_qubits
        next_x = np.cos(next_angle)
        next_y = np.sin(next_angle)
        
        edges.append(dict(
            x=[x, next_x],
            y=[y, next_y],
            mode='lines',
            line=dict(width=2, color='gray'),
            showlegend=False
        ))
    
    fig = go.Figure()
    
    # Add edges
    for edge in edges:
        fig.add_trace(go.Scatter(
            x=edge['x'], y=edge['y'],
            mode=edge['mode'],
            line=edge['line'],
            showlegend=edge['showlegend']
        ))
    
    # Add nodes
    for node in nodes:
        fig.add_trace(go.Scatter(
            x=[node['x']], y=[node['y']],
            mode=node['mode'],
            text=[node['text']],
            marker=node['marker'],
            textposition=node['textposition'],
            name='Qubits'
        ))
    
    fig.update_layout(
        title=f'Quantum Network Topology ({n_qubits} qubits)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
    )
    
    return fig

def create_metrics_display(n_qubits, noise_level):
    """Create real-time metrics display"""
    # Mock metrics
    fidelity = max(0.1, 1 - noise_level * 0.8)
    purity = max(0.1, 1 - noise_level * 0.6)
    entropy = min(1.0, noise_level * 0.7)
    coherence_time = max(0.1, 1 - noise_level * 0.9)
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{fidelity:.3f}", className="text-primary"),
                    html.P("Fidelity", className="text-muted mb-0")
                ])
            ], color="light", outline=True)
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{purity:.3f}", className="text-success"),
                    html.P("Purity", className="text-muted mb-0")
                ])
            ], color="light", outline=True)
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{entropy:.3f}", className="text-warning"),
                    html.P("Entropy", className="text-muted mb-0")
                ])
            ], color="light", outline=True)
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{coherence_time:.3f}", className="text-info"),
                    html.P("Coherence", className="text-muted mb-0")
                ])
            ], color="light", outline=True)
        ], width=3)
    ])
