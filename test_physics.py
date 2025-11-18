#!/usr/bin/python3
"""
Test suite for physics_formulas.py
Simple tests to validate core functionality
"""

from physics_formulas import (
    Kinematics, Dynamics, Energy, Thermodynamics,
    Waves, Electricity, Gravitation, Relativity
)
import math


def test_kinematics():
    """Test kinematics equations."""
    print("Testing Kinematics...")
    
    # Test velocity calculation
    v = Kinematics.velocity_from_acceleration(0, 10, 5)
    assert v == 50, f"Expected 50, got {v}"
    
    # Test displacement
    s = Kinematics.displacement(0, 5, 10)
    assert s == 125.0, f"Expected 125.0, got {s}"
    
    print("✓ Kinematics tests passed")


def test_dynamics():
    """Test dynamics equations."""
    print("Testing Dynamics...")
    
    # Test force calculation
    F = Dynamics.force(10, 5)
    assert F == 50, f"Expected 50, got {F}"
    
    # Test momentum
    p = Dynamics.momentum(5, 10)
    assert p == 50, f"Expected 50, got {p}"
    
    print("✓ Dynamics tests passed")


def test_energy():
    """Test energy equations."""
    print("Testing Energy...")
    
    # Test kinetic energy
    ke = Energy.kinetic_energy(2, 10)
    assert ke == 100.0, f"Expected 100.0, got {ke}"
    
    # Test potential energy
    pe = Energy.potential_energy(10, 10, gravity=10)
    assert pe == 1000, f"Expected 1000, got {pe}"
    
    print("✓ Energy tests passed")


def test_electricity():
    """Test electricity equations."""
    print("Testing Electricity...")
    
    # Test Ohm's law
    V = Electricity.ohms_law_voltage(10, 5)
    assert V == 50, f"Expected 50, got {V}"
    
    I = Electricity.ohms_law_current(50, 5)
    assert I == 10, f"Expected 10, got {I}"
    
    R = Electricity.ohms_law_resistance(50, 10)
    assert R == 5, f"Expected 5, got {R}"
    
    # Test power
    P = Electricity.electrical_power(10, 5)
    assert P == 50, f"Expected 50, got {P}"
    
    print("✓ Electricity tests passed")


def test_thermodynamics():
    """Test thermodynamics equations."""
    print("Testing Thermodynamics...")
    
    # Test ideal gas law
    P = Thermodynamics.ideal_gas_law(volume=1, n_moles=1, temperature=273.15, R=8.314)
    assert abs(P - 2270.97) < 1, f"Expected ~2270.97, got {P}"
    
    # Test heat transfer
    Q = Thermodynamics.heat_transfer(1, 4186, 1)
    assert Q == 4186, f"Expected 4186, got {Q}"
    
    print("✓ Thermodynamics tests passed")


def test_waves():
    """Test wave equations."""
    print("Testing Waves...")
    
    # Test wave speed
    v = Waves.wave_speed(100, 3)
    assert v == 300, f"Expected 300, got {v}"
    
    # Test frequency from period
    f = Waves.frequency_from_period(2)
    assert f == 0.5, f"Expected 0.5, got {f}"
    
    print("✓ Waves tests passed")


def test_gravitation():
    """Test gravitation equations."""
    print("Testing Gravitation...")
    
    # Test gravitational force
    F = Gravitation.gravitational_force(1e6, 1e6, 1, G=6.674e-11)
    expected = 6.674e-11 * 1e6 * 1e6 / 1
    assert abs(F - expected) < 0.01, f"Expected {expected}, got {F}"
    
    print("✓ Gravitation tests passed")


def test_relativity():
    """Test relativity equations."""
    print("Testing Relativity...")
    
    # Test mass-energy equivalence
    E = Relativity.mass_energy_equivalence(1, c=3e8)
    assert E == 9e16, f"Expected 9e16, got {E}"
    
    print("✓ Relativity tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING PHYSICS FORMULAS TESTS")
    print("=" * 60)
    print()
    
    try:
        test_kinematics()
        test_dynamics()
        test_energy()
        test_electricity()
        test_thermodynamics()
        test_waves()
        test_gravitation()
        test_relativity()
        
        print()
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"TEST FAILED ✗")
        print(f"Error: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"UNEXPECTED ERROR ✗")
        print(f"Error: {e}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
