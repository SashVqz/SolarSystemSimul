# entities/planetData.py

import numpy as np
from .celestialBody import CelestialBody
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris
from astropy.time import Time
from astropy.units import km, s, kg
from astropy import constants as const 

# It's good practice to set the ephemeris once globally.
solar_system_ephemeris.set('de432s')

def getSolarSystemBodies(epoch=Time.now()):
    bodies = []

    # --- Sun Data ---
    sun_mass_kg = const.M_sun.to(kg).value
    sun_radius_m = const.R_sun.to(km).value * 1000.0
    bodies.append(CelestialBody("Sun", sun_mass_kg, sun_radius_m,
                                np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]),
                                texturePath="assets/textures/sunTexture.jpg"))

    # --- Mercury ---
    # Hardcode mass and radius for Mercury
    mass_mercury_kg = 3.3011e23 # kg (NASA fact sheet)
    radius_mercury_m = 2439.7 * 1000.0 # meters (NASA fact sheet)
    mercury_posvel = get_body_barycentric_posvel('mercury', epoch, None)
    mercury_pos_m = mercury_posvel[0].xyz.to(km).value * 1000.0
    mercury_vel_m_s = mercury_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Mercury", mass_mercury_kg, radius_mercury_m,
                                mercury_pos_m, mercury_vel_m_s,
                                texturePath="assets/textures/mercuryTexture.jpg"))

    # --- Venus ---
    # Hardcode mass and radius for Venus
    mass_venus_kg = 4.8675e24 # kg (NASA fact sheet)
    radius_venus_m = 6051.8 * 1000.0 # meters (NASA fact sheet)
    venus_posvel = get_body_barycentric_posvel('venus', epoch, None)
    venus_pos_m = venus_posvel[0].xyz.to(km).value * 1000.0
    venus_vel_m_s = venus_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Venus", mass_venus_kg, radius_venus_m,
                                venus_pos_m, venus_vel_m_s,
                                texturePath="assets/textures/venusTexture.jpg"))

    # --- Earth ---
    # Keep Earth's mass and radius from const as they are usually reliable
    earth_mass_kg = const.M_earth.to(kg).value
    earth_radius_m = const.R_earth.to(km).value * 1000.0
    earth_posvel = get_body_barycentric_posvel('earth', epoch, None)
    earth_pos_m = earth_posvel[0].xyz.to(km).value * 1000.0
    earth_vel_m_s = earth_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Earth", earth_mass_kg, earth_radius_m,
                                earth_pos_m, earth_vel_m_s,
                                texturePath="assets/textures/earthTexture.jpg"))

    # --- The Moon (Satellite of Earth) ---
    # Hardcode mass and radius for Moon
    moon_mass_kg = 7.342e22 # kg (NASA fact sheet)
    moon_radius_m = 1737.4 * 1000.0 # meters (NASA fact sheet)
    moon_posvel_ssb = get_body_barycentric_posvel('moon', epoch, None)
    moon_pos_ssb_m = moon_posvel_ssb[0].xyz.to(km).value * 1000.0
    moon_vel_ssb_m_s = moon_posvel_ssb[1].xyz.to(km/s).value * 1000.0
    moon_absolute_pos = moon_pos_ssb_m
    moon_absolute_vel = moon_vel_ssb_m_s
    bodies.append(CelestialBody("Moon", moon_mass_kg, moon_radius_m,
                                moon_absolute_pos, moon_absolute_vel,
                                texturePath="assets/textures/moonTexture.jpg"))

    # --- Mars ---
    # Hardcode mass and radius for Mars
    mass_mars_kg = 6.4171e23 # kg (NASA fact sheet)
    radius_mars_m = 3389.5 * 1000.0 # meters (NASA fact sheet)
    mars_posvel = get_body_barycentric_posvel('mars', epoch, None)
    mars_pos_m = mars_posvel[0].xyz.to(km).value * 1000.0
    mars_vel_m_s = mars_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Mars", mass_mars_kg, radius_mars_m,
                                mars_pos_m, mars_vel_m_s,
                                texturePath="assets/textures/marsTexture.jpg"))

    # --- Jupiter ---
    # Hardcode mass and radius for Jupiter
    jupiter_mass_kg = 1.8982e27 # kg (NASA fact sheet)
    jupiter_radius_m = 71492.0 * 1000.0 # meters (NASA fact sheet)
    jupiter_posvel = get_body_barycentric_posvel('jupiter', epoch, None)
    jupiter_pos_m = jupiter_posvel[0].xyz.to(km).value * 1000.0
    jupiter_vel_m_s = jupiter_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Jupiter", jupiter_mass_kg, jupiter_radius_m,
                                jupiter_pos_m, jupiter_vel_m_s,
                                texturePath="assets/textures/jupiterTexture.jpg"))

    # --- Saturn ---
    # Hardcode mass and radius for Saturn
    saturn_mass_kg = 5.6834e26 # kg (NASA fact sheet)
    saturn_radius_m = 60268.0 * 1000.0 # meters (NASA fact sheet)
    saturn_posvel = get_body_barycentric_posvel('saturn', epoch, None)
    saturn_pos_m = saturn_posvel[0].xyz.to(km).value * 1000.0
    saturn_vel_m_s = saturn_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Saturn", saturn_mass_kg, saturn_radius_m,
                                saturn_pos_m, saturn_vel_m_s,
                                texturePath="assets/textures/saturnTexture.jpg"))

    # --- Uranus ---
    # Hardcode mass and radius for Uranus
    uranus_mass_kg = 8.6810e25 # kg (NASA fact sheet)
    uranus_radius_m = 25559.0 * 1000.0 # meters (NASA fact sheet)
    uranus_posvel = get_body_barycentric_posvel('uranus', epoch, None)
    uranus_pos_m = uranus_posvel[0].xyz.to(km).value * 1000.0
    uranus_vel_m_s = uranus_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Uranus", uranus_mass_kg, uranus_radius_m,
                                uranus_pos_m, uranus_vel_m_s,
                                texturePath="assets/textures/uranusTexture.jpg"))

    # --- Neptune ---
    # Hardcode mass and radius for Neptune
    neptune_mass_kg = 1.02413e26 # kg (NASA fact sheet)
    neptune_radius_m = 24764.0 * 1000.0 # meters (NASA fact sheet)
    neptune_posvel = get_body_barycentric_posvel('neptune', epoch, None)
    neptune_pos_m = neptune_posvel[0].xyz.to(km).value * 1000.0
    neptune_vel_m_s = neptune_posvel[1].xyz.to(km/s).value * 1000.0
    bodies.append(CelestialBody("Neptune", neptune_mass_kg, neptune_radius_m,
                                neptune_pos_m, neptune_vel_m_s,
                                texturePath="assets/textures/neptuneTexture.jpg"))

    return bodies