# pysphere-assignment-1

A comprehensive Python library implementing fundamental physics formulas from research papers and textbooks.

## Features

This repository contains Python implementations of key physics equations across multiple domains:

### 1. Kinematics
- Velocity from acceleration: `v = u + at`
- Displacement: `s = ut + (1/2)at²`
- Final velocity: `v² = u² + 2as`

### 2. Dynamics (Newton's Laws)
- Force: `F = ma`
- Weight: `W = mg`
- Momentum: `p = mv`

### 3. Energy
- Kinetic energy: `KE = (1/2)mv²`
- Potential energy: `PE = mgh`
- Elastic potential energy: `PE = (1/2)kx²`

### 4. Electricity
- Ohm's law: `V = IR`
- Electrical power: `P = VI`
- Capacitance energy: `E = (1/2)CV²`

### 5. Thermodynamics
- Ideal gas law: `PV = nRT`
- Heat transfer: `Q = mcΔT`

### 6. Waves
- Wave speed: `v = fλ`
- Frequency from period: `f = 1/T`
- Photon energy: `E = hf`

### 7. Gravitation
- Gravitational force: `F = G(m₁m₂)/r²`
- Orbital velocity: `v = √(GM/r)`

### 8. Relativity
- Time dilation: `t = t₀/√(1 - v²/c²)`
- Mass-energy equivalence: `E = mc²`
- Relativistic momentum: `p = γmv`

## Usage

### Running the main library demo
```bash
python3 physics_formulas.py
```

### Using specific formulas
```python
from physics_formulas import Kinematics, Energy, Electricity

# Calculate final velocity
velocity = Kinematics.velocity_from_acceleration(
    initial_velocity=10,
    acceleration=2,
    time=5
)

# Calculate kinetic energy
ke = Energy.kinetic_energy(mass=10, velocity=15)

# Calculate voltage using Ohm's law
voltage = Electricity.ohms_law_voltage(current=10, resistance=5)
```

### Legacy Ohm's Law Calculator
The repository also includes a simple interactive Ohm's law calculator:
```bash
python3 ohms_law.py
```

## Files

- `physics_formulas.py` - Main physics library with comprehensive formulas
- `test_physics.py` - Test suite validating all formulas
- `examples.py` - Practical examples demonstrating real-world applications
- `ohms_law.py` - Interactive Ohm's law calculator

## Running Examples

### View practical examples
```bash
python3 examples.py
```

This runs 7 real-world examples:
1. Projectile motion (ball thrown upward)
2. Car acceleration and energy
3. Home electricity calculations
4. Heating water
5. Light wave properties
6. Earth-Moon gravitational system
7. Relativistic space travel

### Run tests
```bash
python3 test_physics.py
```

## Requirements

- Python 3.x
- Standard library only (no external dependencies)