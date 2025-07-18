# config.py

# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Simulation settings
SIMULATION_TIME_STEP_REAL = 3600 * 24 # 1 day in seconds (real-world time step for physics calculations)
TIME_WARP = 500.0                   # How many times faster the simulation runs than real-time (e.g., 100x, 1000x, 10000x)
SIMULATION_TIME_STEP = SIMULATION_TIME_STEP_REAL * TIME_WARP # Effective time step for the simulator

GRAVITATIONAL_CONSTANT = 6.67430e-11 # G constant in m^3 kg^-1 s^-2

# Scaling factors for rendering. Adjust these carefully!
# To make solar system fit in view, positions and radii need scaling.
# 1 AU is approx 1.5e11 meters. If scaled by 1e9, 1 AU becomes 150 units.
POSITION_SCALE_FACTOR = 1.0 / 1_000_000_000_000.0 # 1 trillion meters = 1 unit (for distances)
RADIUS_SCALE_FACTOR = 1.0 / 1_000_000_000.0    # 1 billion meters = 1 unit (for body sizes)

# Camera settings
# Initial position should be adjusted based on POSITION_SCALE_FACTOR
INITIAL_CAMERA_POSITION = [0.0, 0.0, 500.0 * POSITION_SCALE_FACTOR / 1e-9] # Example adjustment
CAMERA_SPEED = 20.0 # Units per second (adjust based on POSITION_SCALE_FACTOR)
MOUSE_SENSITIVITY = 0.1 # For camera rotation

# Sphere procedural generation settings (for planets/moon)
SPHERE_SEGMENTS_X = 64 # Longitude segments
SPHERE_SEGMENTS_Y = 32 # Latitude segments