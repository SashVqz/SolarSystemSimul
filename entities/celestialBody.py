# entities/celestialBody.py

import numpy as np

class CelestialBody:
    def __init__(self, name, mass, radius, initial_position, initial_velocity, texturePath=None):
        self.name = name
        self.mass = float(mass) # kg
        self.radius = float(radius) # meters
        self.position = np.array(initial_position, dtype=np.float64) # meters
        self.velocity = np.array(initial_velocity, dtype=np.float64) # meters/second
        self.texturePath = texturePath
        self.textureId = 0 # OpenGL texture ID, set after loading
        # For Verlet integration: velocity at half time step
        self.velocity_half_step = np.array(initial_velocity, dtype=np.float64)

    def __repr__(self):
        return f"CelestialBody(Name='{self.name}', Mass={self.mass:.2e} kg, Radius={self.radius:.2e} m, Pos={self.position}, Vel={self.velocity})"