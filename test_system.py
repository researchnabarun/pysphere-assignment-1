#!/usr/bin/env python3
"""
Test script for multi-agent control system

This script runs a series of tests to validate the implementation.
"""

import numpy as np
import sys


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...", end=" ")
    try:
        from multiagent_control import (
            MultiAgentSystem, SystemParameters, AgentState,
            create_circular_trajectory, create_linear_trajectory
        )
        from visualize_system import SystemVisualizer, run_simulation_with_visualization
        from examples import (
            example_fixed_time_consensus,
            example_prescribed_time_tracking,
            example_optimal_tracking
        )
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_system_creation():
    """Test that multi-agent system can be created"""
    print("Testing system creation...", end=" ")
    try:
        from multiagent_control import MultiAgentSystem, SystemParameters
        
        params = SystemParameters()
        system = MultiAgentSystem(5, dimension=2, params=params)
        
        assert system.num_agents == 5
        assert system.dimension == 2
        assert len(system.agents) == 5
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_fixed_time_control():
    """Test fixed-time control"""
    print("Testing fixed-time control...", end=" ")
    try:
        from multiagent_control import MultiAgentSystem, SystemParameters, create_circular_trajectory
        
        params = SystemParameters(alpha=1.5, beta=0.5, k1=2.0, k2=1.5)
        system = MultiAgentSystem(3, dimension=2, params=params)
        
        pos_func, vel_func = create_circular_trajectory(radius=5.0, omega=0.5)
        system.set_leader_trajectory(pos_func, vel_func)
        
        # Run simulation
        for i in range(100):
            system.simulate_step(0.01, i*0.01, control_type='fixed_time')
        
        # Control should reduce errors
        error = system.get_consensus_error()
        assert not np.isnan(error) and not np.isinf(error)
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_prescribed_time_control():
    """Test prescribed-time control"""
    print("Testing prescribed-time control...", end=" ")
    try:
        from multiagent_control import MultiAgentSystem, SystemParameters, create_circular_trajectory
        
        params = SystemParameters(prescribed_time=5.0)
        system = MultiAgentSystem(3, dimension=2, params=params)
        
        pos_func, vel_func = create_circular_trajectory(radius=3.0, omega=1.0)
        system.set_leader_trajectory(pos_func, vel_func)
        
        # Run simulation
        for i in range(200):
            system.simulate_step(0.01, i*0.01, control_type='prescribed_time')
        
        # Check no numerical issues
        error = system.get_tracking_error()
        assert not np.isnan(error) and not np.isinf(error)
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_optimal_control():
    """Test optimal tracking control"""
    print("Testing optimal control...", end=" ")
    try:
        from multiagent_control import MultiAgentSystem, SystemParameters, create_linear_trajectory
        
        params = SystemParameters()
        system = MultiAgentSystem(4, dimension=2, params=params)
        
        velocity_vec = np.array([1.0, 0.5])
        pos_func, vel_func = create_linear_trajectory(velocity_vec)
        system.set_leader_trajectory(pos_func, vel_func)
        
        # Run simulation
        for i in range(100):
            system.simulate_step(0.01, i*0.01, control_type='optimal')
        
        error = system.get_tracking_error()
        assert not np.isnan(error) and not np.isinf(error)
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_fault_tolerance():
    """Test fault tolerance mechanism"""
    print("Testing fault tolerance...", end=" ")
    try:
        from multiagent_control import MultiAgentSystem, SystemParameters
        
        system = MultiAgentSystem(5, dimension=2)
        
        # Introduce faults
        system.introduce_fault(0, fault_severity=0.5)
        system.introduce_fault(2, fault_severity=0.2)
        
        assert system.agents[0].fault_factor == 0.5
        assert system.agents[2].fault_factor == 0.2
        assert system.agents[1].fault_factor == 1.0  # No fault
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_communication_topology():
    """Test custom communication topology"""
    print("Testing communication topology...", end=" ")
    try:
        from multiagent_control import MultiAgentSystem
        
        # Create custom adjacency matrix (ring topology)
        num_agents = 5
        adjacency = np.zeros((num_agents, num_agents))
        for i in range(num_agents):
            adjacency[i, (i + 1) % num_agents] = 1
            adjacency[i, (i - 1) % num_agents] = 1
        
        system = MultiAgentSystem(num_agents, dimension=2, adjacency_matrix=adjacency)
        
        # Check Laplacian is computed
        assert system.laplacian is not None
        assert system.laplacian.shape == (num_agents, num_agents)
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_trajectory_generation():
    """Test trajectory generation functions"""
    print("Testing trajectory generation...", end=" ")
    try:
        from multiagent_control import create_circular_trajectory, create_linear_trajectory
        
        # Test circular trajectory
        pos_func, vel_func = create_circular_trajectory(radius=5.0, omega=1.0)
        pos = pos_func(0)
        vel = vel_func(0)
        assert len(pos) == 2
        assert len(vel) == 2
        
        # Test linear trajectory
        velocity_vec = np.array([1.0, 2.0])
        pos_func2, vel_func2 = create_linear_trajectory(velocity_vec)
        pos2 = pos_func2(5.0)
        vel2 = vel_func2(5.0)
        assert np.allclose(pos2, velocity_vec * 5.0)
        assert np.allclose(vel2, velocity_vec)
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("MULTI-AGENT CONTROL SYSTEM - TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        test_imports,
        test_system_creation,
        test_fixed_time_control,
        test_prescribed_time_control,
        test_optimal_control,
        test_fault_tolerance,
        test_communication_topology,
        test_trajectory_generation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
