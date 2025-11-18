#!/usr/bin/python3
"""
Example usage of the physics_formulas library.
This demonstrates various practical applications of the formulas.
"""

from physics_formulas import (
    Kinematics, Dynamics, Energy, Thermodynamics,
    Waves, Electricity, Gravitation, Relativity
)


def example_projectile_motion():
    """Example: Calculate projectile motion parameters."""
    print("EXAMPLE 1: Projectile Motion")
    print("-" * 50)
    print("A ball is thrown upward with initial velocity 20 m/s")
    
    initial_velocity = 20  # m/s
    acceleration = -9.81   # m/s² (gravity, downward)
    
    # Time to reach maximum height (when v = 0)
    time_to_max = -initial_velocity / acceleration
    print(f"Time to reach maximum height: {time_to_max:.2f} s")
    
    # Maximum height
    max_height = Kinematics.displacement(initial_velocity, time_to_max, acceleration)
    print(f"Maximum height: {max_height:.2f} m")
    
    # Velocity after 1 second
    v_after_1s = Kinematics.velocity_from_acceleration(initial_velocity, acceleration, 1)
    print(f"Velocity after 1 second: {v_after_1s:.2f} m/s")
    print()


def example_car_acceleration():
    """Example: Calculate force and energy for a car."""
    print("EXAMPLE 2: Car Acceleration")
    print("-" * 50)
    print("A 1500 kg car accelerates from 0 to 100 km/h (27.78 m/s)")
    
    mass = 1500  # kg
    final_velocity = 27.78  # m/s (100 km/h)
    time = 10  # seconds
    
    # Calculate acceleration
    acceleration = final_velocity / time
    print(f"Acceleration: {acceleration:.2f} m/s²")
    
    # Calculate force required
    force = Dynamics.force(mass, acceleration)
    print(f"Force required: {force:.2f} N")
    
    # Calculate final kinetic energy
    ke = Energy.kinetic_energy(mass, final_velocity)
    print(f"Kinetic energy at 100 km/h: {ke:.2f} J ({ke/1000:.2f} kJ)")
    print()


def example_home_electricity():
    """Example: Calculate home electricity usage."""
    print("EXAMPLE 3: Home Electricity")
    print("-" * 50)
    print("A 220V electric heater draws 10A of current")
    
    voltage = 220  # V
    current = 10   # A
    
    # Calculate resistance
    resistance = Electricity.ohms_law_resistance(voltage, current)
    print(f"Heater resistance: {resistance:.2f} Ω")
    
    # Calculate power consumption
    power = Electricity.electrical_power(voltage, current)
    print(f"Power consumption: {power} W ({power/1000} kW)")
    
    # Energy consumed in 2 hours
    hours = 2
    energy_kwh = (power / 1000) * hours
    print(f"Energy in 2 hours: {energy_kwh} kWh")
    print()


def example_heating_water():
    """Example: Calculate energy to heat water."""
    print("EXAMPLE 4: Heating Water")
    print("-" * 50)
    print("Heat 2 liters (2 kg) of water from 20°C to 100°C")
    
    mass = 2  # kg
    specific_heat_water = 4186  # J/(kg⋅K)
    temp_change = 100 - 20  # °C
    
    # Calculate heat required
    heat = Thermodynamics.heat_transfer(mass, specific_heat_water, temp_change)
    print(f"Heat required: {heat} J ({heat/1000:.2f} kJ)")
    
    # If using a 2000W heater
    power = 2000  # W
    time_seconds = heat / power
    time_minutes = time_seconds / 60
    print(f"Time with 2000W heater: {time_minutes:.2f} minutes")
    print()


def example_light_properties():
    """Example: Calculate properties of light."""
    print("EXAMPLE 5: Light Properties")
    print("-" * 50)
    print("Visible light with wavelength 500 nm (green)")
    
    wavelength = 500e-9  # m (500 nanometers)
    speed_of_light = 3e8  # m/s
    
    # Calculate frequency
    frequency = speed_of_light / wavelength
    print(f"Frequency: {frequency:.2e} Hz")
    
    # Calculate photon energy
    energy = Waves.photon_energy(frequency)
    print(f"Photon energy: {energy:.2e} J")
    
    # Convert to electron volts (1 eV = 1.6e-19 J)
    energy_ev = energy / 1.6e-19
    print(f"Photon energy: {energy_ev:.2f} eV")
    print()


def example_earth_moon():
    """Example: Calculate gravitational force between Earth and Moon."""
    print("EXAMPLE 6: Earth-Moon System")
    print("-" * 50)
    
    earth_mass = 5.972e24  # kg
    moon_mass = 7.342e22   # kg
    distance = 3.844e8     # m (average distance)
    
    # Calculate gravitational force
    force = Gravitation.gravitational_force(earth_mass, moon_mass, distance)
    print(f"Gravitational force: {force:.2e} N")
    
    # Calculate Moon's orbital velocity
    orbital_v = Gravitation.orbital_velocity(earth_mass, distance)
    print(f"Moon's orbital velocity: {orbital_v:.2f} m/s ({orbital_v/1000:.2f} km/s)")
    print()


def example_space_travel():
    """Example: Calculate relativistic effects for space travel."""
    print("EXAMPLE 7: Relativistic Space Travel")
    print("-" * 50)
    print("Spacecraft traveling at 0.9c (90% speed of light)")
    
    velocity = 0.9 * 3e8  # m/s
    proper_time = 1  # year in spacecraft frame
    
    # Calculate time dilation
    dilated_time = Relativity.time_dilation(proper_time, velocity)
    print(f"1 year on spacecraft = {dilated_time:.2f} years on Earth")
    
    # Mass-energy equivalence for 1 kg
    mass = 1  # kg
    energy = Relativity.mass_energy_equivalence(mass)
    print(f"Energy equivalent of 1 kg: {energy:.2e} J")
    
    # Compare to Hiroshima bomb (~63 TJ)
    hiroshima = 63e12  # J
    bombs = energy / hiroshima
    print(f"Equivalent to {bombs:.0f} Hiroshima bombs")
    print()


def main():
    """Run all examples."""
    print("=" * 60)
    print("PHYSICS FORMULAS - PRACTICAL EXAMPLES")
    print("=" * 60)
    print()
    
    example_projectile_motion()
    example_car_acceleration()
    example_home_electricity()
    example_heating_water()
    example_light_properties()
    example_earth_moon()
    example_space_travel()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
