# Multi-Agent Control System

Python implementation of **Fixed-Time and Prescribed Time Fault-Tolerant Optimal Tracking Control for Heterogeneous Multiagent Systems** based on the IEEE paper.

## Overview

This repository implements advanced control algorithms for multi-agent systems with the following features:

- **Fixed-Time Consensus**: Convergence within a fixed time regardless of initial conditions
- **Prescribed-Time Consensus**: Convergence within a user-specified time
- **Fault-Tolerant Control**: Handles actuator faults and failures
- **Optimal Tracking**: Follows desired trajectories while minimizing control effort
- **Heterogeneous Agents**: Supports agents with different dynamics

## Features

### Control Protocols

1. **Fixed-Time Control**
   - Uses nonlinear feedback: `u = -k1·sig^α(e) - k2·sig^β(e)`
   - Converges in fixed time regardless of initial conditions
   - Parameters: α > 1, 0 < β < 1

2. **Prescribed-Time Control**
   - Uses time-varying gains: `u(t) = -ρ(t)·k·e(t)`
   - Converges exactly at user-specified time Tp
   - Scaling function: `ρ(t) = exp(a·t/(Tp-t))`

3. **Optimal Tracking Control**
   - Minimizes cost function: `J = ∫(e^T·Q·e + u^T·R·u)dt`
   - LQR-like approach for heterogeneous agents
   - Balances tracking accuracy and control effort

### Fault Tolerance

- Adaptive fault detection and estimation
- Compensation for partial actuator failures
- Maintains performance under faulty conditions
- Supports multiple simultaneous faults

## Installation

### Prerequisites

- Python 3.7 or higher
- NumPy
- Matplotlib

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from multiagent_control import MultiAgentSystem, SystemParameters, create_circular_trajectory

# Create a multi-agent system with 5 agents
num_agents = 5
params = SystemParameters(alpha=1.5, beta=0.5, k1=2.0, k2=1.5)
system = MultiAgentSystem(num_agents, dimension=2, params=params)

# Set leader trajectory
pos_func, vel_func = create_circular_trajectory(radius=5.0, omega=0.5)
system.set_leader_trajectory(pos_func, vel_func)

# Simulation
dt = 0.01
t_final = 10.0

for step in range(int(t_final / dt)):
    t = step * dt
    system.simulate_step(dt, t, control_type='fixed_time')

print(f"Consensus error: {system.get_consensus_error():.6f}")
print(f"Tracking error: {system.get_tracking_error():.6f}")
```

### Running Examples

```bash
# Run basic examples
python examples.py

# Run simulation with visualization
python visualize_system.py

# Run the main multiagent control demo
python multiagent_control.py
```

### Introducing Faults

```python
# Introduce a fault to agent 2 with 50% effectiveness
system.introduce_fault(agent_idx=2, fault_severity=0.5)
```

## Project Structure

```
.
├── multiagent_control.py    # Core control algorithms
├── visualize_system.py      # Visualization utilities
├── examples.py              # Example scenarios
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── ohms_law.py            # Original assignment file
```

## Control Algorithms

### Fixed-Time Consensus

The fixed-time control law ensures convergence within a finite time T_max that is independent of initial conditions:

```
T_max ≤ (1/(k1(α-1))) + (1/(k2(1-β)))
```

### Prescribed-Time Consensus

The prescribed-time control guarantees convergence at exactly time Tp:

```
lim_{t→Tp} e(t) = 0
```

### Fault Model

Actuator faults are modeled as:

```
u_actual = ρ(t) · u_desired
```

where ρ(t) ∈ [0,1] is the fault factor (1 = healthy, 0 = complete failure).

## System Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `alpha` | Fixed-time parameter | 1.5 | > 1 |
| `beta` | Fixed-time parameter | 0.5 | (0, 1) |
| `k1` | Control gain 1 | 2.0 | > 0 |
| `k2` | Control gain 2 | 1.5 | > 0 |
| `gamma` | Fault compensation | 0.5 | > 0 |
| `prescribed_time` | Target convergence time | 10.0 | > 0 |

## Visualization

The `visualize_system.py` module generates:

1. **Trajectory plots**: Agent paths in 2D space
2. **Error plots**: Consensus and tracking errors over time
3. **Fault plots**: Fault factors for each agent

Example output files:
- `fixed_time_simulation_trajectories.png`
- `fixed_time_simulation_errors.png`
- `fixed_time_simulation_faults.png`

## Examples

### Example 1: Fixed-Time Consensus
```bash
python -c "from examples import example_fixed_time_consensus; example_fixed_time_consensus()"
```

### Example 2: Prescribed-Time Tracking
```bash
python -c "from examples import example_prescribed_time_tracking; example_prescribed_time_tracking()"
```

### Example 3: Optimal Tracking
```bash
python -c "from examples import example_optimal_tracking; example_optimal_tracking()"
```

### Example 4: Control Comparison
```bash
python -c "from examples import example_control_comparison; example_control_comparison()"
```

### Example 5: Large-Scale System
```bash
python -c "from examples import example_large_scale; example_large_scale()"
```

## Mathematical Background

### Communication Topology

The system uses a graph Laplacian L to represent communication:

```
L = D - A
```

where D is the degree matrix and A is the adjacency matrix.

### Consensus Error

```
e_i = Σ_j a_ij(x_i - x_j) + (x_i - x_leader)
```

### Lyapunov Stability

All control laws are designed using Lyapunov theory to guarantee:
- Stability
- Convergence
- Finite/prescribed time convergence

## Performance Characteristics

### Fixed-Time Control
- ✓ Convergence time independent of initial conditions
- ✓ Robust to disturbances
- ✓ Suitable for time-critical applications

### Prescribed-Time Control
- ✓ Exact convergence at specified time
- ✓ User-definable convergence time
- ✓ Predictable behavior

### Optimal Tracking
- ✓ Minimizes control effort
- ✓ Balances tracking and energy
- ✓ Suitable for resource-constrained systems

## References

Based on the IEEE paper:
**"Fixed-Time and Prescribed Time Fault-Tolerant Optimal Tracking Control for Heterogeneous Multiagent Systems"**

Key concepts:
- Fixed-time stability theory
- Prescribed-time control
- Fault-tolerant consensus
- Optimal cooperative control
- Multi-agent coordination

## License

This is an educational implementation for research purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Author

Research implementation for PySphere Assignment

## Acknowledgments

- IEEE paper authors for the theoretical foundation
- NumPy and Matplotlib communities