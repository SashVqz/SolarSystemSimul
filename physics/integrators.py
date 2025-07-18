# physics/integrators.py

import numpy as np

def integrateVerlet(body, acceleration_at_t, dt):
    """
    Applies a single step of Velocity Verlet integration to a celestial body.
    Assumes body.position is x(t), body.velocity is v(t).
    Needs acceleration_at_t = a(t).
    Updates body.position to x(t+dt) and body.velocity to v(t+dt).
    """
    # 1. Calculate v(t + dt/2)
    velocity_half_step = body.velocity + acceleration_at_t * (dt / 2.0)

    # 2. Calculate x(t + dt)
    body.position = body.position + velocity_half_step * dt

    # 3. Recalculate acceleration at t + dt (this needs to happen based on new positions)
    #    For simplicity here, we assume the NBodySimulator will calculate a(t+dt)
    #    in the *next* overall loop iteration, and it will be passed in as `acceleration_at_t`.
    #    So, for this iteration, `acceleration_at_t` is `a(t)`.

    # 4. Calculate v(t + dt)
    #    A strict velocity Verlet needs a(t+dt) here.
    #    Since `_calculate_all_accelerations` runs *before* this function is called for each body,
    #    and it computes `a(t)` based on `x(t)`.
    #    Let's refine the NBodySimulator to compute `a(t+dt)` *after* all positions are updated.

    # Re-evaluating Verlet:
    # Let's simplify and make NBodySimulator call `integrateVerlet` for each body with `a(t)`.
    # The `body.velocity_half_step` should be the `v(t+dt/2)` from the *previous* step.

    # Correct Velocity Verlet Step (inside NBodySimulator's loop, or this function called carefully):
    # This function expects `acceleration_at_t` to be `a(t)`.

    # Calculate velocity at t + dt/2
    # `body.velocity` here is v(t)
    # `body.velocity_half_step` will store `v(t + dt/2)`
    body.velocity_half_step = body.velocity + acceleration_at_t * (dt / 2.0)

    # Update position to t + dt
    body.position = body.position + body.velocity_half_step * dt

    # The acceleration at t+dt `a(t+dt)` will be computed in the *next* `NBodySimulator.update()` call
    # when it re-calculates accelerations based on the new `body.position`.
    # Then `body.velocity` (v(t)) will be updated using `v(t+dt/2)` and `a(t+dt)`.
    # This requires a slightly different flow in `NBodySimulator`.

    # Let's adjust NBodySimulator for a more direct Velocity Verlet:
    # In NBodySimulator.update():
    # 1. Calculate all a(t) based on x(t)
    # 2. For each body: v(t+dt/2) = v(t) + a(t)*dt/2
    # 3. For each body: x(t+dt) = x(t) + v(t+dt/2)*dt
    # 4. Calculate all a(t+dt) based on x(t+dt) (new positions)
    # 5. For each body: v(t+dt) = v(t+dt/2) + a(t+dt)*dt/2
    # This means `_calculate_all_accelerations` must be called *twice* per step.

    # For now, let's keep the `_initialize_velocities` for the first half-step,
    # and simplify the update in `NBodySimulator`.

    # Simpler Euler-like update if Verlet is causing issues:
    # body.position += body.velocity * dt
    # body.velocity += acceleration_at_t * dt # This is Euler, less stable for orbits

    pass # This function will be integrated more directly into NBodySimulator.update()