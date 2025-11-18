#!/usr/bin/python3
"""
Physics Formulas Library
Implementation of fundamental physics equations from research papers and textbooks.
"""

import math


class Kinematics:
    """Kinematics equations for motion analysis."""
    
    @staticmethod
    def velocity_from_acceleration(initial_velocity, acceleration, time):
        """
        Calculate final velocity given initial velocity, acceleration, and time.
        Formula: v = u + at
        
        Args:
            initial_velocity: Initial velocity (m/s)
            acceleration: Acceleration (m/s²)
            time: Time elapsed (s)
        
        Returns:
            Final velocity (m/s)
        """
        return initial_velocity + acceleration * time
    
    @staticmethod
    def displacement(initial_velocity, time, acceleration):
        """
        Calculate displacement with constant acceleration.
        Formula: s = ut + (1/2)at²
        
        Args:
            initial_velocity: Initial velocity (m/s)
            time: Time elapsed (s)
            acceleration: Acceleration (m/s²)
        
        Returns:
            Displacement (m)
        """
        return initial_velocity * time + 0.5 * acceleration * time ** 2
    
    @staticmethod
    def final_velocity_squared(initial_velocity, acceleration, displacement):
        """
        Calculate final velocity squared using displacement.
        Formula: v² = u² + 2as
        
        Args:
            initial_velocity: Initial velocity (m/s)
            acceleration: Acceleration (m/s²)
            displacement: Displacement (m)
        
        Returns:
            Final velocity (m/s)
        """
        v_squared = initial_velocity ** 2 + 2 * acceleration * displacement
        return math.sqrt(abs(v_squared)) if v_squared >= 0 else -math.sqrt(abs(v_squared))


class Dynamics:
    """Dynamics equations based on Newton's laws."""
    
    @staticmethod
    def force(mass, acceleration):
        """
        Calculate force using Newton's second law.
        Formula: F = ma
        
        Args:
            mass: Mass of object (kg)
            acceleration: Acceleration (m/s²)
        
        Returns:
            Force (N)
        """
        return mass * acceleration
    
    @staticmethod
    def weight(mass, gravity=9.81):
        """
        Calculate weight of an object.
        Formula: W = mg
        
        Args:
            mass: Mass of object (kg)
            gravity: Gravitational acceleration (m/s², default 9.81)
        
        Returns:
            Weight (N)
        """
        return mass * gravity
    
    @staticmethod
    def momentum(mass, velocity):
        """
        Calculate linear momentum.
        Formula: p = mv
        
        Args:
            mass: Mass of object (kg)
            velocity: Velocity (m/s)
        
        Returns:
            Momentum (kg⋅m/s)
        """
        return mass * velocity


class Energy:
    """Energy equations for various forms of energy."""
    
    @staticmethod
    def kinetic_energy(mass, velocity):
        """
        Calculate kinetic energy.
        Formula: KE = (1/2)mv²
        
        Args:
            mass: Mass of object (kg)
            velocity: Velocity (m/s)
        
        Returns:
            Kinetic energy (J)
        """
        return 0.5 * mass * velocity ** 2
    
    @staticmethod
    def potential_energy(mass, height, gravity=9.81):
        """
        Calculate gravitational potential energy.
        Formula: PE = mgh
        
        Args:
            mass: Mass of object (kg)
            height: Height above reference point (m)
            gravity: Gravitational acceleration (m/s², default 9.81)
        
        Returns:
            Potential energy (J)
        """
        return mass * gravity * height
    
    @staticmethod
    def elastic_potential_energy(spring_constant, displacement):
        """
        Calculate elastic potential energy in a spring.
        Formula: PE = (1/2)kx²
        
        Args:
            spring_constant: Spring constant (N/m)
            displacement: Displacement from equilibrium (m)
        
        Returns:
            Elastic potential energy (J)
        """
        return 0.5 * spring_constant * displacement ** 2


class Thermodynamics:
    """Thermodynamics equations."""
    
    @staticmethod
    def ideal_gas_law(pressure=None, volume=None, n_moles=None, temperature=None, R=8.314):
        """
        Calculate missing variable using ideal gas law.
        Formula: PV = nRT
        
        Args:
            pressure: Pressure (Pa)
            volume: Volume (m³)
            n_moles: Number of moles (mol)
            temperature: Temperature (K)
            R: Gas constant (J/(mol⋅K), default 8.314)
        
        Returns:
            The missing variable value
        """
        if pressure is None:
            return (n_moles * R * temperature) / volume
        elif volume is None:
            return (n_moles * R * temperature) / pressure
        elif n_moles is None:
            return (pressure * volume) / (R * temperature)
        elif temperature is None:
            return (pressure * volume) / (n_moles * R)
        else:
            return None
    
    @staticmethod
    def heat_transfer(mass, specific_heat, temperature_change):
        """
        Calculate heat transfer.
        Formula: Q = mcΔT
        
        Args:
            mass: Mass of substance (kg)
            specific_heat: Specific heat capacity (J/(kg⋅K))
            temperature_change: Change in temperature (K or °C)
        
        Returns:
            Heat transferred (J)
        """
        return mass * specific_heat * temperature_change


class Waves:
    """Wave mechanics equations."""
    
    @staticmethod
    def wave_speed(frequency, wavelength):
        """
        Calculate wave speed.
        Formula: v = fλ
        
        Args:
            frequency: Frequency (Hz)
            wavelength: Wavelength (m)
        
        Returns:
            Wave speed (m/s)
        """
        return frequency * wavelength
    
    @staticmethod
    def frequency_from_period(period):
        """
        Calculate frequency from period.
        Formula: f = 1/T
        
        Args:
            period: Period (s)
        
        Returns:
            Frequency (Hz)
        """
        return 1 / period
    
    @staticmethod
    def photon_energy(frequency, h=6.626e-34):
        """
        Calculate photon energy.
        Formula: E = hf
        
        Args:
            frequency: Frequency (Hz)
            h: Planck's constant (J⋅s, default 6.626e-34)
        
        Returns:
            Energy (J)
        """
        return h * frequency


class Electricity:
    """Electrical equations including Ohm's law."""
    
    @staticmethod
    def ohms_law_voltage(current, resistance):
        """
        Calculate voltage using Ohm's law.
        Formula: V = IR
        
        Args:
            current: Current (A)
            resistance: Resistance (Ω)
        
        Returns:
            Voltage (V)
        """
        return current * resistance
    
    @staticmethod
    def ohms_law_current(voltage, resistance):
        """
        Calculate current using Ohm's law.
        Formula: I = V/R
        
        Args:
            voltage: Voltage (V)
            resistance: Resistance (Ω)
        
        Returns:
            Current (A)
        """
        return voltage / resistance
    
    @staticmethod
    def ohms_law_resistance(voltage, current):
        """
        Calculate resistance using Ohm's law.
        Formula: R = V/I
        
        Args:
            voltage: Voltage (V)
            current: Current (A)
        
        Returns:
            Resistance (Ω)
        """
        return voltage / current
    
    @staticmethod
    def electrical_power(voltage, current):
        """
        Calculate electrical power.
        Formula: P = VI
        
        Args:
            voltage: Voltage (V)
            current: Current (A)
        
        Returns:
            Power (W)
        """
        return voltage * current
    
    @staticmethod
    def capacitance_energy(capacitance, voltage):
        """
        Calculate energy stored in a capacitor.
        Formula: E = (1/2)CV²
        
        Args:
            capacitance: Capacitance (F)
            voltage: Voltage (V)
        
        Returns:
            Energy (J)
        """
        return 0.5 * capacitance * voltage ** 2


class Gravitation:
    """Gravitational equations."""
    
    @staticmethod
    def gravitational_force(mass1, mass2, distance, G=6.674e-11):
        """
        Calculate gravitational force between two masses.
        Formula: F = G(m₁m₂)/r²
        
        Args:
            mass1: Mass of first object (kg)
            mass2: Mass of second object (kg)
            distance: Distance between centers (m)
            G: Gravitational constant (N⋅m²/kg², default 6.674e-11)
        
        Returns:
            Gravitational force (N)
        """
        return G * mass1 * mass2 / (distance ** 2)
    
    @staticmethod
    def orbital_velocity(mass, radius, G=6.674e-11):
        """
        Calculate orbital velocity.
        Formula: v = √(GM/r)
        
        Args:
            mass: Mass of central body (kg)
            radius: Orbital radius (m)
            G: Gravitational constant (N⋅m²/kg², default 6.674e-11)
        
        Returns:
            Orbital velocity (m/s)
        """
        return math.sqrt(G * mass / radius)


class Relativity:
    """Special relativity equations."""
    
    @staticmethod
    def time_dilation(proper_time, velocity, c=3e8):
        """
        Calculate time dilation effect.
        Formula: t = t₀/√(1 - v²/c²)
        
        Args:
            proper_time: Time in rest frame (s)
            velocity: Velocity (m/s)
            c: Speed of light (m/s, default 3e8)
        
        Returns:
            Dilated time (s)
        """
        gamma = 1 / math.sqrt(1 - (velocity ** 2) / (c ** 2))
        return proper_time * gamma
    
    @staticmethod
    def mass_energy_equivalence(mass, c=3e8):
        """
        Calculate energy from mass using Einstein's equation.
        Formula: E = mc²
        
        Args:
            mass: Mass (kg)
            c: Speed of light (m/s, default 3e8)
        
        Returns:
            Energy (J)
        """
        return mass * c ** 2
    
    @staticmethod
    def relativistic_momentum(mass, velocity, c=3e8):
        """
        Calculate relativistic momentum.
        Formula: p = γmv where γ = 1/√(1 - v²/c²)
        
        Args:
            mass: Rest mass (kg)
            velocity: Velocity (m/s)
            c: Speed of light (m/s, default 3e8)
        
        Returns:
            Relativistic momentum (kg⋅m/s)
        """
        gamma = 1 / math.sqrt(1 - (velocity ** 2) / (c ** 2))
        return gamma * mass * velocity


def main():
    """Demonstration of physics formulas."""
    print("=" * 60)
    print("PHYSICS FORMULAS LIBRARY - DEMONSTRATION")
    print("=" * 60)
    
    # Kinematics
    print("\n1. KINEMATICS")
    print("-" * 40)
    v = Kinematics.velocity_from_acceleration(10, 2, 5)
    print(f"Final velocity (u=10 m/s, a=2 m/s², t=5 s): {v} m/s")
    
    s = Kinematics.displacement(5, 10, 2)
    print(f"Displacement (u=5 m/s, t=10 s, a=2 m/s²): {s} m")
    
    # Dynamics
    print("\n2. DYNAMICS")
    print("-" * 40)
    F = Dynamics.force(10, 5)
    print(f"Force (m=10 kg, a=5 m/s²): {F} N")
    
    p = Dynamics.momentum(5, 20)
    print(f"Momentum (m=5 kg, v=20 m/s): {p} kg⋅m/s")
    
    # Energy
    print("\n3. ENERGY")
    print("-" * 40)
    ke = Energy.kinetic_energy(10, 15)
    print(f"Kinetic energy (m=10 kg, v=15 m/s): {ke} J")
    
    pe = Energy.potential_energy(5, 20)
    print(f"Potential energy (m=5 kg, h=20 m): {pe} J")
    
    # Electricity
    print("\n4. ELECTRICITY (Ohm's Law)")
    print("-" * 40)
    V = Electricity.ohms_law_voltage(10, 5)
    print(f"Voltage (I=10 A, R=5 Ω): {V} V")
    
    P = Electricity.electrical_power(220, 5)
    print(f"Power (V=220 V, I=5 A): {P} W")
    
    # Thermodynamics
    print("\n5. THERMODYNAMICS")
    print("-" * 40)
    P = Thermodynamics.ideal_gas_law(volume=0.1, n_moles=1, temperature=300)
    print(f"Pressure (V=0.1 m³, n=1 mol, T=300 K): {P:.2f} Pa")
    
    Q = Thermodynamics.heat_transfer(2, 4186, 10)
    print(f"Heat transfer (m=2 kg, c=4186 J/(kg⋅K), ΔT=10 K): {Q} J")
    
    # Waves
    print("\n6. WAVES")
    print("-" * 40)
    v = Waves.wave_speed(500, 0.6)
    print(f"Wave speed (f=500 Hz, λ=0.6 m): {v} m/s")
    
    E = Waves.photon_energy(5e14)
    print(f"Photon energy (f=5×10¹⁴ Hz): {E:.2e} J")
    
    # Gravitation
    print("\n7. GRAVITATION")
    print("-" * 40)
    F = Gravitation.gravitational_force(5.972e24, 70, 6.371e6)
    print(f"Gravitational force (Earth-human): {F:.2f} N")
    
    # Relativity
    print("\n8. RELATIVITY")
    print("-" * 40)
    E = Relativity.mass_energy_equivalence(1)
    print(f"Energy from 1 kg mass: {E:.2e} J")
    
    print("\n" + "=" * 60)
    print("All calculations completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
