#!/usr/bin/env python3
"""
Visualization utilities for multi-agent control system

This module provides functions to visualize the behavior of the multi-agent
system including trajectories, consensus errors, and tracking performance.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
from multiagent_control import (
    MultiAgentSystem, SystemParameters, 
    create_circular_trajectory, create_linear_trajectory
)


class SystemVisualizer:
    """Visualizer for multi-agent control systems"""
    
    def __init__(self, system: MultiAgentSystem):
        """
        Initialize the visualizer
        
        Args:
            system: Multi-agent system to visualize
        """
        self.system = system
        self.history = {
            'time': [],
            'positions': [],
            'velocities': [],
            'consensus_errors': [],
            'tracking_errors': [],
            'fault_factors': []
        }
    
    def record_state(self, t: float):
        """
        Record current system state
        
        Args:
            t: Current time
        """
        self.history['time'].append(t)
        
        # Record positions
        positions = [agent.position.copy() for agent in self.system.agents]
        self.history['positions'].append(positions)
        
        # Record velocities
        velocities = [agent.velocity.copy() for agent in self.system.agents]
        self.history['velocities'].append(velocities)
        
        # Record errors
        self.history['consensus_errors'].append(self.system.get_consensus_error())
        self.history['tracking_errors'].append(self.system.get_tracking_error())
        
        # Record fault factors
        fault_factors = [agent.fault_factor for agent in self.system.agents]
        self.history['fault_factors'].append(fault_factors)
    
    def plot_trajectories(self, save_path: Optional[str] = None):
        """
        Plot agent trajectories in 2D space
        
        Args:
            save_path: Path to save the figure (if None, display instead)
        """
        if self.system.dimension != 2:
            print("Trajectory plot only supports 2D systems")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot each agent's trajectory
        for i in range(self.system.num_agents):
            positions = [pos[i] for pos in self.history['positions']]
            x = [p[0] for p in positions]
            y = [p[1] for p in positions]
            
            # Plot trajectory
            ax.plot(x, y, '-', alpha=0.6, label=f'Agent {i}')
            
            # Mark start and end
            ax.plot(x[0], y[0], 'o', markersize=8)
            ax.plot(x[-1], y[-1], 's', markersize=8)
        
        # Plot leader trajectory if available
        if hasattr(self.system, 'leader_position_func'):
            times = np.array(self.history['time'])
            leader_positions = [self.system.leader_position_func(t) for t in times]
            leader_x = [p[0] for p in leader_positions]
            leader_y = [p[1] for p in leader_positions]
            ax.plot(leader_x, leader_y, 'k--', linewidth=2, label='Leader', alpha=0.7)
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_title('Agent Trajectories')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Trajectory plot saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_errors(self, save_path: Optional[str] = None):
        """
        Plot consensus and tracking errors over time
        
        Args:
            save_path: Path to save the figure (if None, display instead)
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        times = np.array(self.history['time'])
        
        # Consensus error
        ax1.plot(times, self.history['consensus_errors'], 'b-', linewidth=2)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Consensus Error')
        ax1.set_title('Consensus Error Over Time')
        ax1.grid(True, alpha=0.3)
        
        # Tracking error
        ax2.plot(times, self.history['tracking_errors'], 'r-', linewidth=2)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Average Tracking Error')
        ax2.set_title('Tracking Error Over Time')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Error plot saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_fault_factors(self, save_path: Optional[str] = None):
        """
        Plot fault factors for all agents over time
        
        Args:
            save_path: Path to save the figure (if None, display instead)
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        times = np.array(self.history['time'])
        
        for i in range(self.system.num_agents):
            fault_factors = [ff[i] for ff in self.history['fault_factors']]
            ax.plot(times, fault_factors, linewidth=2, label=f'Agent {i}')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Fault Factor (1=No Fault, 0=Complete Fault)')
        ax.set_title('Agent Fault Factors Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim([-0.1, 1.1])
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Fault factor plot saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_all(self, prefix: str = 'multiagent'):
        """
        Generate all plots and save to files
        
        Args:
            prefix: Prefix for saved filenames
        """
        self.plot_trajectories(f'{prefix}_trajectories.png')
        self.plot_errors(f'{prefix}_errors.png')
        self.plot_fault_factors(f'{prefix}_faults.png')


def run_simulation_with_visualization(
    num_agents: int = 5,
    control_type: str = 'fixed_time',
    t_final: float = 15.0,
    dt: float = 0.01,
    introduce_fault: bool = True,
    fault_agent: int = 2,
    fault_time: float = 5.0,
    fault_severity: float = 0.5
):
    """
    Run a complete simulation with visualization
    
    Args:
        num_agents: Number of agents
        control_type: Type of control ('fixed_time', 'prescribed_time', 'optimal')
        t_final: Final simulation time
        dt: Time step
        introduce_fault: Whether to introduce a fault
        fault_agent: Agent to introduce fault to
        fault_time: Time to introduce fault
        fault_severity: Severity of fault (0-1)
    """
    print(f"Multi-Agent Control System Simulation")
    print("=" * 70)
    print(f"Control Type: {control_type}")
    print(f"Number of Agents: {num_agents}")
    print(f"Simulation Duration: {t_final}s")
    print(f"Time Step: {dt}s")
    
    # Create system
    params = SystemParameters(
        alpha=1.5,
        beta=0.5,
        k1=2.0,
        k2=1.5,
        prescribed_time=10.0
    )
    
    system = MultiAgentSystem(num_agents, dimension=2, params=params)
    
    # Set leader trajectory
    pos_func, vel_func = create_circular_trajectory(radius=5.0, omega=0.5)
    system.set_leader_trajectory(pos_func, vel_func)
    
    # Create visualizer
    visualizer = SystemVisualizer(system)
    
    # Simulation
    fault_introduced = False
    steps = int(t_final / dt)
    
    print("\nRunning simulation...")
    for step in range(steps):
        t = step * dt
        
        # Introduce fault
        if introduce_fault and t >= fault_time and not fault_introduced:
            print(f"\n[t={t:.2f}s] Introducing fault to Agent {fault_agent} "
                  f"(severity: {fault_severity})")
            system.introduce_fault(fault_agent, fault_severity)
            fault_introduced = True
        
        # Simulate step
        system.simulate_step(dt, t, control_type=control_type)
        
        # Record state
        if step % int(0.1 / dt) == 0:  # Record every 0.1s
            visualizer.record_state(t)
        
        # Print progress
        if step % int(1.0 / dt) == 0:
            consensus_error = system.get_consensus_error()
            tracking_error = system.get_tracking_error()
            print(f"t={t:6.2f}s | Consensus: {consensus_error:8.4f} | "
                  f"Tracking: {tracking_error:8.4f}")
    
    print("\nSimulation completed!")
    
    # Generate plots
    print("\nGenerating visualizations...")
    visualizer.plot_all(prefix=f'{control_type}_simulation')
    
    print("\nFinal Statistics:")
    print(f"Final Consensus Error: {system.get_consensus_error():.6f}")
    print(f"Final Tracking Error: {system.get_tracking_error():.6f}")
    
    return system, visualizer


if __name__ == "__main__":
    # Run simulation with fixed-time control
    print("\n" + "=" * 70)
    print("FIXED-TIME CONTROL SIMULATION")
    print("=" * 70)
    system1, vis1 = run_simulation_with_visualization(
        num_agents=5,
        control_type='fixed_time',
        t_final=15.0,
        introduce_fault=True
    )
    
    print("\n" + "=" * 70)
    print("PRESCRIBED-TIME CONTROL SIMULATION")
    print("=" * 70)
    system2, vis2 = run_simulation_with_visualization(
        num_agents=5,
        control_type='prescribed_time',
        t_final=15.0,
        introduce_fault=True
    )
    
    print("\n" + "=" * 70)
    print("OPTIMAL TRACKING CONTROL SIMULATION")
    print("=" * 70)
    system3, vis3 = run_simulation_with_visualization(
        num_agents=5,
        control_type='optimal',
        t_final=15.0,
        introduce_fault=True
    )
    
    print("\nAll simulations completed successfully!")
    print("Check the generated PNG files for visualizations.")
