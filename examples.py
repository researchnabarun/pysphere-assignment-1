"""
Configuration and Examples for Multi-Agent Control System

This module provides example configurations and use cases for the
fixed-time and prescribed-time fault-tolerant control system.
"""

import numpy as np
from multiagent_control import (
    MultiAgentSystem, SystemParameters, AgentState,
    create_circular_trajectory, create_linear_trajectory
)


# Example 1: Fixed-time consensus with fault tolerance
def example_fixed_time_consensus():
    """
    Demonstrate fixed-time consensus protocol with fault introduction
    """
    print("\nExample 1: Fixed-Time Consensus with Fault Tolerance")
    print("-" * 60)
    
    # Create system
    num_agents = 4
    params = SystemParameters(
        alpha=1.5,
        beta=0.5,
        k1=2.0,
        k2=1.5
    )
    
    system = MultiAgentSystem(num_agents, dimension=2, params=params)
    
    # Set leader trajectory (stationary at origin)
    pos_func = lambda t: np.array([0.0, 0.0])
    vel_func = lambda t: np.array([0.0, 0.0])
    system.set_leader_trajectory(pos_func, vel_func)
    
    # Simulation
    dt = 0.01
    t_final = 10.0
    
    print(f"Initial positions:")
    for i, agent in enumerate(system.agents):
        print(f"  Agent {i}: {agent.position}")
    
    # Run simulation
    for step in range(int(t_final / dt)):
        t = step * dt
        
        # Introduce fault at t=5s
        if abs(t - 5.0) < dt:
            print(f"\nFault introduced to Agent 1 at t={t:.2f}s")
            system.introduce_fault(1, fault_severity=0.3)
        
        system.simulate_step(dt, t, control_type='fixed_time')
    
    print(f"\nFinal positions (after {t_final}s):")
    for i, agent in enumerate(system.agents):
        print(f"  Agent {i}: {agent.position} (fault: {agent.fault_factor:.2f})")
    
    print(f"\nFinal consensus error: {system.get_consensus_error():.6f}")
    print(f"Final tracking error: {system.get_tracking_error():.6f}")


# Example 2: Prescribed-time tracking control
def example_prescribed_time_tracking():
    """
    Demonstrate prescribed-time tracking of a circular trajectory
    """
    print("\nExample 2: Prescribed-Time Tracking Control")
    print("-" * 60)
    
    # Create system with prescribed time = 8 seconds
    num_agents = 6
    params = SystemParameters(
        alpha=1.5,
        beta=0.5,
        k1=2.0,
        k2=1.5,
        prescribed_time=8.0
    )
    
    system = MultiAgentSystem(num_agents, dimension=2, params=params)
    
    # Set circular trajectory
    pos_func, vel_func = create_circular_trajectory(radius=3.0, omega=1.0)
    system.set_leader_trajectory(pos_func, vel_func)
    
    # Simulation
    dt = 0.01
    t_final = 10.0
    
    print(f"Prescribed convergence time: {params.prescribed_time}s")
    print(f"Number of agents: {num_agents}")
    
    # Track errors over time
    errors = []
    times = []
    
    for step in range(int(t_final / dt)):
        t = step * dt
        system.simulate_step(dt, t, control_type='prescribed_time')
        
        if step % int(0.5 / dt) == 0:
            error = system.get_tracking_error()
            errors.append(error)
            times.append(t)
            print(f"t={t:5.2f}s | Tracking Error: {error:8.6f}")
    
    print(f"\nError at prescribed time ({params.prescribed_time}s): "
          f"{errors[int(params.prescribed_time / 0.5)]:.6f}")
    print(f"Final error: {errors[-1]:.6f}")


# Example 3: Optimal tracking with heterogeneous agents
def example_optimal_tracking():
    """
    Demonstrate optimal tracking control for heterogeneous agents
    """
    print("\nExample 3: Optimal Tracking Control (Heterogeneous Agents)")
    print("-" * 60)
    
    # Create system
    num_agents = 5
    params = SystemParameters(
        k1=3.0,
        k2=2.0
    )
    
    # Custom adjacency matrix (not fully connected)
    # Ring topology: each agent connects to its neighbors
    adjacency = np.zeros((num_agents, num_agents))
    for i in range(num_agents):
        adjacency[i, (i + 1) % num_agents] = 1
        adjacency[i, (i - 1) % num_agents] = 1
    
    system = MultiAgentSystem(num_agents, dimension=2, 
                             adjacency_matrix=adjacency, params=params)
    
    # Set linear trajectory
    velocity_vec = np.array([1.0, 0.5])
    pos_func, vel_func = create_linear_trajectory(velocity_vec)
    system.set_leader_trajectory(pos_func, vel_func)
    
    print("Communication topology: Ring (each agent connects to 2 neighbors)")
    
    # Simulation
    dt = 0.01
    t_final = 12.0
    
    for step in range(int(t_final / dt)):
        t = step * dt
        
        # Introduce multiple faults
        if abs(t - 3.0) < dt:
            system.introduce_fault(1, fault_severity=0.6)
            print(f"\nt={t:.2f}s: Fault on Agent 1 (60% capacity)")
        
        if abs(t - 7.0) < dt:
            system.introduce_fault(3, fault_severity=0.4)
            print(f"t={t:.2f}s: Fault on Agent 3 (40% capacity)")
        
        system.simulate_step(dt, t, control_type='optimal')
        
        if step % int(1.0 / dt) == 0:
            consensus = system.get_consensus_error()
            tracking = system.get_tracking_error()
            print(f"t={t:5.2f}s | Consensus: {consensus:6.4f} | "
                  f"Tracking: {tracking:6.4f}")
    
    print(f"\nFinal state:")
    for i, agent in enumerate(system.agents):
        print(f"  Agent {i}: pos={agent.position}, "
              f"fault_factor={agent.fault_factor:.2f}")


# Example 4: Comparison of control methods
def example_control_comparison():
    """
    Compare different control methods on the same scenario
    """
    print("\nExample 4: Comparison of Control Methods")
    print("-" * 60)
    
    num_agents = 4
    dimension = 2
    dt = 0.01
    t_final = 10.0
    
    # Common setup
    params = SystemParameters(
        alpha=1.5,
        beta=0.5,
        k1=2.0,
        k2=1.5,
        prescribed_time=8.0
    )
    
    pos_func, vel_func = create_circular_trajectory(radius=4.0, omega=0.8)
    
    # Test each control type
    control_types = ['fixed_time', 'prescribed_time', 'optimal']
    results = {}
    
    for control_type in control_types:
        print(f"\nTesting {control_type} control...")
        
        # Create fresh system
        system = MultiAgentSystem(num_agents, dimension, params=params)
        system.set_leader_trajectory(pos_func, vel_func)
        
        # Set same initial conditions
        np.random.seed(42)
        for i in range(num_agents):
            system.agents[i].position = np.random.randn(dimension) * 3
            system.agents[i].velocity = np.random.randn(dimension) * 0.5
        
        # Introduce fault
        system.introduce_fault(2, fault_severity=0.5)
        
        # Simulate
        final_consensus = 0.0
        final_tracking = 0.0
        
        for step in range(int(t_final / dt)):
            t = step * dt
            system.simulate_step(dt, t, control_type=control_type)
        
        final_consensus = system.get_consensus_error()
        final_tracking = system.get_tracking_error()
        
        results[control_type] = {
            'consensus': final_consensus,
            'tracking': final_tracking
        }
        
        print(f"  Final consensus error: {final_consensus:.6f}")
        print(f"  Final tracking error: {final_tracking:.6f}")
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"{'Control Type':<20} {'Consensus Error':<20} {'Tracking Error':<20}")
    print("-" * 60)
    for control_type, result in results.items():
        print(f"{control_type:<20} {result['consensus']:<20.6f} "
              f"{result['tracking']:<20.6f}")


# Example 5: Large-scale system
def example_large_scale():
    """
    Demonstrate scalability with a large number of agents
    """
    print("\nExample 5: Large-Scale Multi-Agent System")
    print("-" * 60)
    
    num_agents = 20
    params = SystemParameters(
        alpha=1.5,
        beta=0.5,
        k1=1.5,
        k2=1.0
    )
    
    system = MultiAgentSystem(num_agents, dimension=2, params=params)
    
    # Circular trajectory
    pos_func, vel_func = create_circular_trajectory(radius=6.0, omega=0.6)
    system.set_leader_trajectory(pos_func, vel_func)
    
    print(f"Number of agents: {num_agents}")
    print(f"Communication links: {int(np.sum(system.adjacency_matrix))}")
    
    # Simulation
    dt = 0.01
    t_final = 15.0
    
    # Introduce faults to multiple agents
    fault_agents = [5, 10, 15]
    fault_severities = [0.7, 0.5, 0.3]
    
    for step in range(int(t_final / dt)):
        t = step * dt
        
        # Introduce faults at different times
        if abs(t - 5.0) < dt:
            for agent_idx, severity in zip(fault_agents, fault_severities):
                system.introduce_fault(agent_idx, severity)
            print(f"\nt={t:.2f}s: Faults introduced to agents {fault_agents}")
        
        system.simulate_step(dt, t, control_type='fixed_time')
        
        if step % int(2.0 / dt) == 0:
            consensus = system.get_consensus_error()
            tracking = system.get_tracking_error()
            print(f"t={t:5.2f}s | Consensus: {consensus:8.4f} | "
                  f"Tracking: {tracking:8.4f}")
    
    print(f"\nFinal consensus error: {system.get_consensus_error():.6f}")
    print(f"Final tracking error: {system.get_tracking_error():.6f}")


if __name__ == "__main__":
    print("=" * 60)
    print("MULTI-AGENT CONTROL SYSTEM - EXAMPLES")
    print("=" * 60)
    
    # Run all examples
    example_fixed_time_consensus()
    print("\n" + "=" * 60)
    
    example_prescribed_time_tracking()
    print("\n" + "=" * 60)
    
    example_optimal_tracking()
    print("\n" + "=" * 60)
    
    example_control_comparison()
    print("\n" + "=" * 60)
    
    example_large_scale()
    print("\n" + "=" * 60)
    
    print("\nAll examples completed successfully!")
