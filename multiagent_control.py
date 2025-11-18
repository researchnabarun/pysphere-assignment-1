#!/usr/bin/env python3
"""
Fixed-Time and Prescribed Time Fault-Tolerant Optimal Tracking Control
for Heterogeneous Multiagent Systems

This module implements the control algorithms described in the IEEE paper:
- Fixed-time consensus protocol
- Prescribed-time consensus protocol
- Fault-tolerant mechanisms
- Optimal tracking control for heterogeneous multi-agent systems
"""

import numpy as np
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass


@dataclass
class AgentState:
    """Represents the state of a single agent"""
    position: np.ndarray
    velocity: np.ndarray
    fault_factor: float = 1.0  # 1.0 = no fault, 0.0 = complete fault
    
    
@dataclass
class SystemParameters:
    """Parameters for the multi-agent control system"""
    alpha: float = 1.5  # Fixed-time parameter (α > 1)
    beta: float = 0.5   # Fixed-time parameter (0 < β < 1)
    k1: float = 1.0     # Control gain 1
    k2: float = 1.0     # Control gain 2
    gamma: float = 0.5  # Fault compensation parameter
    prescribed_time: float = 10.0  # Prescribed convergence time (Tp)
    

class MultiAgentSystem:
    """
    Multi-agent system with fixed-time and prescribed-time control
    """
    
    def __init__(self, 
                 num_agents: int,
                 dimension: int = 2,
                 adjacency_matrix: Optional[np.ndarray] = None,
                 params: Optional[SystemParameters] = None):
        """
        Initialize the multi-agent system
        
        Args:
            num_agents: Number of agents in the system
            dimension: State dimension for each agent
            adjacency_matrix: Communication topology (if None, uses all-to-all)
            params: System parameters
        """
        self.num_agents = num_agents
        self.dimension = dimension
        self.params = params if params is not None else SystemParameters()
        
        # Initialize agent states
        self.agents: List[AgentState] = []
        for i in range(num_agents):
            position = np.random.randn(dimension)
            velocity = np.random.randn(dimension)
            self.agents.append(AgentState(position, velocity))
        
        # Set up communication topology (adjacency matrix)
        if adjacency_matrix is not None:
            self.adjacency_matrix = adjacency_matrix
        else:
            # Default: all-to-all communication (excluding self-loops)
            self.adjacency_matrix = np.ones((num_agents, num_agents)) - np.eye(num_agents)
        
        # Compute Laplacian matrix
        self._compute_laplacian()
        
        # Leader trajectory (if applicable)
        self.leader_position = np.zeros(dimension)
        self.leader_velocity = np.zeros(dimension)
        
    def _compute_laplacian(self):
        """Compute the graph Laplacian matrix"""
        degree_matrix = np.diag(np.sum(self.adjacency_matrix, axis=1))
        self.laplacian = degree_matrix - self.adjacency_matrix
        
    def set_leader_trajectory(self, position_func: Callable[[float], np.ndarray],
                             velocity_func: Callable[[float], np.ndarray]):
        """
        Set the leader's trajectory functions
        
        Args:
            position_func: Function that returns leader position at time t
            velocity_func: Function that returns leader velocity at time t
        """
        self.leader_position_func = position_func
        self.leader_velocity_func = velocity_func
        
    def update_leader(self, t: float):
        """Update leader state at time t"""
        if hasattr(self, 'leader_position_func'):
            self.leader_position = self.leader_position_func(t)
            self.leader_velocity = self.leader_velocity_func(t)
    
    def fixed_time_control(self, agent_idx: int, t: float) -> np.ndarray:
        """
        Compute fixed-time control input for an agent
        
        The control law ensures convergence within a fixed time regardless
        of initial conditions using nonlinear feedback.
        
        Args:
            agent_idx: Index of the agent
            t: Current time
            
        Returns:
            Control input vector
        """
        alpha = self.params.alpha
        beta = self.params.beta
        k1 = self.params.k1
        k2 = self.params.k2
        
        # Get current agent state
        agent = self.agents[agent_idx]
        
        # Compute consensus error (relative to neighbors)
        consensus_error = np.zeros(self.dimension)
        for j in range(self.num_agents):
            if self.adjacency_matrix[agent_idx, j] > 0:
                consensus_error += self.adjacency_matrix[agent_idx, j] * (
                    agent.position - self.agents[j].position
                )
        
        # Tracking error (relative to leader)
        tracking_error = agent.position - self.leader_position
        
        # Combined error
        total_error = consensus_error + tracking_error
        
        # Fixed-time control law with nonlinear terms
        # u = -k1 * sig^α(e) - k2 * sig^β(e)
        # where sig^p(x) = |x|^p * sign(x)
        control = -(k1 * self._sig_power(total_error, alpha) + 
                   k2 * self._sig_power(total_error, beta))
        
        # Apply fault compensation
        control = control / (agent.fault_factor + 1e-6)
        
        return control
    
    def prescribed_time_control(self, agent_idx: int, t: float) -> np.ndarray:
        """
        Compute prescribed-time control input for an agent
        
        The control law ensures convergence within a user-specified time Tp
        using time-varying gains.
        
        Args:
            agent_idx: Index of the agent
            t: Current time
            
        Returns:
            Control input vector
        """
        Tp = self.params.prescribed_time
        
        # Time-varying scaling function
        # ρ(t) = exp(a * t / (Tp - t)) for t < Tp
        if t >= Tp - 0.01:  # Near prescribed time
            rho_t = 1e6  # Large value to ensure convergence
        else:
            a = 2.0
            rho_t = np.exp(a * t / (Tp - t))
        
        # Get current agent state
        agent = self.agents[agent_idx]
        
        # Compute consensus error
        consensus_error = np.zeros(self.dimension)
        for j in range(self.num_agents):
            if self.adjacency_matrix[agent_idx, j] > 0:
                consensus_error += self.adjacency_matrix[agent_idx, j] * (
                    agent.position - self.agents[j].position
                )
        
        # Tracking error
        tracking_error = agent.position - self.leader_position
        
        # Combined error
        total_error = consensus_error + tracking_error
        
        # Prescribed-time control law with time-varying gain
        # u(t) = -ρ(t) * k * e(t)
        k = self.params.k1
        control = -rho_t * k * total_error
        
        # Apply fault compensation
        control = control / (agent.fault_factor + 1e-6)
        
        return control
    
    def optimal_tracking_control(self, agent_idx: int, t: float) -> np.ndarray:
        """
        Compute optimal tracking control that minimizes a cost function
        
        The control minimizes J = ∫(e^T Q e + u^T R u)dt
        
        Args:
            agent_idx: Index of the agent
            t: Current time
            
        Returns:
            Optimal control input vector
        """
        # State and control weight matrices
        Q = np.eye(self.dimension)  # State error weight
        R = np.eye(self.dimension)  # Control effort weight
        
        agent = self.agents[agent_idx]
        
        # Tracking error
        tracking_error = agent.position - self.leader_position
        velocity_error = agent.velocity - self.leader_velocity
        
        # Consensus error
        consensus_error = np.zeros(self.dimension)
        for j in range(self.num_agents):
            if self.adjacency_matrix[agent_idx, j] > 0:
                consensus_error += self.adjacency_matrix[agent_idx, j] * (
                    agent.position - self.agents[j].position
                )
        
        # Combined error
        total_error = tracking_error + consensus_error
        
        # Optimal control law (LQR-like)
        # u = -R^(-1) * B^T * P * e
        # Simplified version: u = -K * (position_error + velocity_error)
        K = np.linalg.inv(R) @ Q
        control = -K @ (total_error + 0.5 * velocity_error)
        
        # Apply fault compensation
        control = control / (agent.fault_factor + 1e-6)
        
        return control
    
    def fault_detection_and_estimation(self, agent_idx: int, 
                                      control_input: np.ndarray,
                                      actual_output: np.ndarray) -> float:
        """
        Estimate the fault factor for an agent
        
        Args:
            agent_idx: Index of the agent
            control_input: Applied control input
            actual_output: Actual system output/acceleration
            
        Returns:
            Estimated fault factor (1.0 = no fault, 0.0 = complete fault)
        """
        # Expected output under no fault condition
        expected_output = control_input
        
        # Fault estimation based on output error
        output_error = np.linalg.norm(actual_output - expected_output)
        
        # Estimate fault factor using adaptive law
        gamma = self.params.gamma
        fault_estimate = 1.0 - gamma * output_error
        
        # Bound the fault factor
        fault_estimate = np.clip(fault_estimate, 0.1, 1.0)
        
        return fault_estimate
    
    def simulate_step(self, dt: float, t: float, 
                     control_type: str = 'fixed_time') -> None:
        """
        Simulate one time step of the multi-agent system
        
        Args:
            dt: Time step
            t: Current time
            control_type: Type of control ('fixed_time', 'prescribed_time', or 'optimal')
        """
        # Update leader trajectory
        self.update_leader(t)
        
        # Compute control inputs for all agents
        controls = []
        for i in range(self.num_agents):
            if control_type == 'fixed_time':
                u = self.fixed_time_control(i, t)
            elif control_type == 'prescribed_time':
                u = self.prescribed_time_control(i, t)
            elif control_type == 'optimal':
                u = self.optimal_tracking_control(i, t)
            else:
                raise ValueError(f"Unknown control type: {control_type}")
            controls.append(u)
        
        # Update agent states (simple integrator dynamics: ẋ = u)
        for i in range(self.num_agents):
            # Update velocity (acceleration from control)
            self.agents[i].velocity += controls[i] * dt
            
            # Update position
            self.agents[i].position += self.agents[i].velocity * dt
    
    def introduce_fault(self, agent_idx: int, fault_severity: float):
        """
        Introduce a fault to an agent
        
        Args:
            agent_idx: Index of the agent
            fault_severity: Fault severity (0.0 = complete fault, 1.0 = no fault)
        """
        self.agents[agent_idx].fault_factor = np.clip(fault_severity, 0.0, 1.0)
    
    def get_consensus_error(self) -> float:
        """
        Compute the consensus error of the system
        
        Returns:
            Total consensus error
        """
        consensus_error = 0.0
        for i in range(self.num_agents):
            for j in range(i + 1, self.num_agents):
                error = np.linalg.norm(
                    self.agents[i].position - self.agents[j].position
                )
                consensus_error += error
        return consensus_error
    
    def get_tracking_error(self) -> float:
        """
        Compute the tracking error relative to leader
        
        Returns:
            Average tracking error
        """
        total_error = 0.0
        for agent in self.agents:
            error = np.linalg.norm(agent.position - self.leader_position)
            total_error += error
        return total_error / self.num_agents
    
    @staticmethod
    def _sig_power(x: np.ndarray, p: float) -> np.ndarray:
        """
        Compute sig^p(x) = |x|^p * sign(x) element-wise
        
        Args:
            x: Input vector
            p: Power parameter
            
        Returns:
            sig^p(x)
        """
        return np.power(np.abs(x), p) * np.sign(x)


def create_circular_trajectory(radius: float = 5.0, 
                               omega: float = 0.5) -> Tuple[Callable, Callable]:
    """
    Create a circular trajectory for the leader
    
    Args:
        radius: Radius of the circle
        omega: Angular velocity
        
    Returns:
        Tuple of (position_function, velocity_function)
    """
    def position(t):
        return np.array([
            radius * np.cos(omega * t),
            radius * np.sin(omega * t)
        ])
    
    def velocity(t):
        return np.array([
            -radius * omega * np.sin(omega * t),
            radius * omega * np.cos(omega * t)
        ])
    
    return position, velocity


def create_linear_trajectory(velocity_vec: np.ndarray) -> Tuple[Callable, Callable]:
    """
    Create a linear trajectory for the leader
    
    Args:
        velocity_vec: Constant velocity vector
        
    Returns:
        Tuple of (position_function, velocity_function)
    """
    def position(t):
        return velocity_vec * t
    
    def velocity(t):
        return velocity_vec
    
    return position, velocity


if __name__ == "__main__":
    # Example usage
    print("Multi-Agent Control System - Fixed-Time and Prescribed-Time Control")
    print("=" * 70)
    
    # Create a multi-agent system with 5 agents
    num_agents = 5
    dimension = 2
    
    # Create system with custom parameters
    params = SystemParameters(
        alpha=1.5,
        beta=0.5,
        k1=2.0,
        k2=1.5,
        prescribed_time=10.0
    )
    
    system = MultiAgentSystem(num_agents, dimension, params=params)
    
    # Set circular trajectory for leader
    pos_func, vel_func = create_circular_trajectory(radius=5.0, omega=0.5)
    system.set_leader_trajectory(pos_func, vel_func)
    
    # Simulation parameters
    dt = 0.01
    t_final = 15.0
    t = 0.0
    
    print(f"\nSimulating {num_agents} agents with fixed-time control...")
    print(f"Simulation time: {t_final} seconds")
    print(f"Time step: {dt} seconds")
    
    # Introduce a fault to agent 2 at t=5s
    fault_time = 5.0
    fault_introduced = False
    
    # Run simulation
    steps = int(t_final / dt)
    for step in range(steps):
        t = step * dt
        
        # Introduce fault at specified time
        if t >= fault_time and not fault_introduced:
            print(f"\n[t={t:.2f}s] Introducing fault to Agent 2 (50% effectiveness)")
            system.introduce_fault(2, fault_severity=0.5)
            fault_introduced = True
        
        # Simulate one step
        system.simulate_step(dt, t, control_type='fixed_time')
        
        # Print status every second
        if step % int(1.0 / dt) == 0:
            consensus_error = system.get_consensus_error()
            tracking_error = system.get_tracking_error()
            print(f"t={t:6.2f}s | Consensus Error: {consensus_error:8.4f} | "
                  f"Tracking Error: {tracking_error:8.4f}")
    
    print("\nSimulation completed!")
    print("\nFinal agent positions:")
    for i, agent in enumerate(system.agents):
        print(f"Agent {i}: {agent.position}, Fault Factor: {agent.fault_factor:.2f}")
    print(f"Leader position: {system.leader_position}")
