#!/usr/bin/env python3
"""
Quick Start Guide for Multi-Agent Control System

This guide provides quick examples to get started with the multi-agent control system.
"""

def quick_start_fixed_time():
    """Quick start example for fixed-time control"""
    from multiagent_control import MultiAgentSystem, SystemParameters, create_circular_trajectory
    
    # Create system
    params = SystemParameters(alpha=1.5, beta=0.5, k1=2.0, k2=1.5)
    system = MultiAgentSystem(num_agents=5, dimension=2, params=params)
    
    # Set leader trajectory
    pos_func, vel_func = create_circular_trajectory(radius=5.0, omega=0.5)
    system.set_leader_trajectory(pos_func, vel_func)
    
    # Run simulation
    dt = 0.01
    for step in range(1000):
        t = step * dt
        system.simulate_step(dt, t, control_type='fixed_time')
    
    print(f"Final consensus error: {system.get_consensus_error():.6f}")
    print(f"Final tracking error: {system.get_tracking_error():.6f}")


def quick_start_with_visualization():
    """Quick start with visualization"""
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    
    from visualize_system import run_simulation_with_visualization
    
    # Run simulation with visualization
    system, visualizer = run_simulation_with_visualization(
        num_agents=5,
        control_type='fixed_time',
        t_final=10.0,
        introduce_fault=True,
        fault_agent=2,
        fault_time=5.0,
        fault_severity=0.5
    )
    
    print("Visualization files saved!")


def quick_start_comparison():
    """Quick comparison of all control methods"""
    from multiagent_control import MultiAgentSystem, SystemParameters, create_circular_trajectory
    import numpy as np
    
    results = {}
    control_types = ['fixed_time', 'prescribed_time', 'optimal']
    
    for control_type in control_types:
        params = SystemParameters()
        system = MultiAgentSystem(4, dimension=2, params=params)
        
        pos_func, vel_func = create_circular_trajectory(radius=4.0, omega=0.8)
        system.set_leader_trajectory(pos_func, vel_func)
        
        # Run simulation
        for step in range(1000):
            system.simulate_step(0.01, step*0.01, control_type=control_type)
        
        results[control_type] = {
            'consensus': system.get_consensus_error(),
            'tracking': system.get_tracking_error()
        }
    
    # Print comparison
    print("\nControl Method Comparison:")
    print("-" * 60)
    for method, res in results.items():
        print(f"{method:20s}: Consensus={res['consensus']:.4f}, Tracking={res['tracking']:.4f}")


if __name__ == "__main__":
    print("=" * 70)
    print("QUICK START GUIDE - Multi-Agent Control System")
    print("=" * 70)
    print()
    
    print("Example 1: Fixed-Time Control")
    print("-" * 70)
    quick_start_fixed_time()
    
    print("\n" + "=" * 70)
    print("Example 2: Control Method Comparison")
    print("-" * 70)
    quick_start_comparison()
    
    print("\n" + "=" * 70)
    print("Example 3: With Visualization")
    print("-" * 70)
    quick_start_with_visualization()
    
    print("\n" + "=" * 70)
    print("Quick start examples completed!")
    print("For more examples, run: python examples.py")
    print("=" * 70)
