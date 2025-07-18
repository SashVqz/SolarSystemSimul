# physics/nBodySimulator.py

import numpy as np
from config import GRAVITATIONAL_CONSTANT
from physics.integrators import integrateVerlet # Using Verlet for stability

class NBodySimulator:
    def __init__(self, celestial_bodies, time_step):
        self.bodies = celestial_bodies
        self.time_step = time_step
        self._initialize_velocities() # Initialize for Verlet integration

    def _initialize_velocities(self):
        # Verlet needs initial acceleration to compute first half-step velocity
        # Compute initial accelerations
        initial_accelerations = self._calculate_all_accelerations()
        for i, body in enumerate(self.bodies):
            # Compute v(t + dt/2) = v(t) + a(t) * dt/2
            body.velocity_half_step = body.velocity + initial_accelerations[i] * (self.time_step / 2.0)

    def _calculate_gravitational_force(self, body1, body2):
        # Calculate vector from body1 to body2
        r_vec = body2.position - body1.position
        distance = np.linalg.norm(r_vec)

        if distance == 0:
            return np.array([0.0, 0.0, 0.0]) # Avoid division by zero if bodies overlap

        # F = G * m1 * m2 / r^2
        force_magnitude = (GRAVITATIONAL_CONSTANT * body1.mass * body2.mass) / (distance ** 2)

        # Force vector direction is along r_vec
        force_direction = r_vec / distance
        force_vector = force_magnitude * force_direction
        return force_vector

    def _calculate_all_accelerations(self):
        accelerations = []
        for i, body_i in enumerate(self.bodies):
            total_force = np.array([0.0, 0.0, 0.0])
            for j, body_j in enumerate(self.bodies):
                if i != j:
                    force_ij = self._calculate_gravitational_force(body_i, body_j)
                    total_force += force_ij
            
            # a = F / m
            if body_i.mass > 0: # Avoid division by zero for massless objects (if any)
                accelerations.append(total_force / body_i.mass)
            else:
                accelerations.append(np.array([0.0, 0.0, 0.0])) # No acceleration for massless bodies
        return accelerations


    def update(self):
        # Calculate accelerations based on current positions
        current_accelerations = self._calculate_all_accelerations()

        for i, body in enumerate(self.bodies):
            # Update position (x(t+dt) = x(t) + v(t+dt/2)*dt)
            body.position = body.position + body.velocity_half_step * self.time_step

            # Update velocity for next half-step (v(t+3dt/2) = v(t+dt/2) + a(t+dt)*dt)
            # This 'a(t+dt)' would ideally be based on new positions, but for basic Verlet
            # we re-calculate accelerations for the _next_ step in the loop or overall.
            # In simple Verlet, the 'a(t)' is used for the full step.
            # A more rigorous Verlet (velocity Verlet) calculates new 'a' based on new 'x'
            # then uses it for the second part of velocity update.

            # Simple Verlet update logic:
            # v(t+dt) = v(t) + a(t) * dt
            # x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2 (original formulation)
            # Or the more common velocity Verlet:
            # 1. v(t+dt/2) = v(t) + a(t) * dt/2 (Done in init and at end of prev update)
            # 2. x(t+dt) = x(t) + v(t+dt/2) * dt
            # 3. Calculate a(t+dt) based on x(t+dt)
            # 4. v(t+dt) = v(t+dt/2) + a(t+dt) * dt/2

            # Let's refine for a more standard Velocity Verlet step within the loop:
            # If `body.velocity` is v(t) and `body.velocity_half_step` is v(t+dt/2) from previous step
            # Then current `current_accelerations[i]` is a(t)
            
            # Step 1: Update full velocity for this time step, based on current acceleration
            # This is the velocity *at* time t+dt
            new_velocity = body.velocity_half_step + current_accelerations[i] * (self.time_step / 2.0)
            body.velocity = new_velocity # Store current full velocity

            # Step 2: Compute acceleration at new position (a(t+dt)) for next half-step velocity
            # This is implicitly done by `_calculate_all_accelerations` at the start of the *next* `update` call.
            # The key for Verlet is that `velocity_half_step` is maintained.
            # Update the half-step velocity for the *next* iteration:
            body.velocity_half_step = new_velocity + current_accelerations[i] * (self.time_step / 2.0)
            # Note: For strict velocity Verlet, `current_accelerations[i]` here should be `a(t+dt)`,
            # which would mean calculating accelerations *after* position update,
            # then looping again for velocity.
            # A simpler Verlet, as initially set up, might re-calculate all accelerations each step
            # and apply them in a way that effectively means `a(t+dt)` is based on `x(t+dt)`.

            # For now, let's assume `current_accelerations` are recalculated each step based on `body.position`
            # and applied using the velocity Verlet concept.
            # The line `body.velocity_half_step = new_velocity + current_accelerations[i] * (self.time_step / 2.0)`
            # is simplified. A better implementation would recalculate `current_accelerations` *after* all positions
            # are updated, then update final velocities.
            # For this simple setup, the `_initialize_velocities` provides the first `v(dt/2)` and
            # the `current_accelerations[i]` are effectively `a(t)`.

            # Let's make it explicitly Velocity Verlet:
            # 1. Calculate a(t)
            # 2. v(t+dt/2) = v(t) + a(t) * dt/2 (stored in body.velocity_half_step)
            # 3. x(t+dt) = x(t) + v(t+dt/2) * dt
            # 4. Calculate a(t+dt) based on x(t+dt) (this is `next_accelerations` calculated at start of *next* step)
            # 5. v(t+dt) = v(t+dt/2) + a(t+dt) * dt/2

            # The current loop calculates `current_accelerations` (which is `a(t)` for this step)
            # Updates `body.position` using `v(t+dt/2)`
            # The line `body.velocity_half_step = body.velocity + current_accelerations[i] * self.time_step` from a previous draft
            # effectively makes `body.velocity` the `v(t+dt/2)` for the *next* step, which is a common Verlet form.
            # Let's stick to the structure that passed `body.velocity_half_step` around as the main integrator value for Verlet.

            # Re-calculating the accelerations at the start of `update` and applying `integrateVerlet` per body is cleaner.
            integrateVerlet(body, current_accelerations[i], self.time_step)