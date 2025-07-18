# entities/ringData.py

class RingData:
    def __init__(self, innerRadius, outerRadius, texturePath, tiltDegrees):
        self.innerRadius = float(innerRadius) # meters
        self.outerRadius = float(outerRadius) # meters
        self.texturePath = texturePath
        self.textureId = None
        self.tiltDegrees = float(tiltDegrees) # Degrees

def getSaturnRingData():
    # Radii of Saturn's A and B rings (main visible rings)
    # B ring inner radius: ~92,000 km from Saturn's center
    # A ring outer radius: ~140,220 km from Saturn's center (main visible rings)
    # The E ring extends much further but is very faint.
    inner_radius_m = 92000 * 1000.0
    outer_radius_m = 140220 * 1000.0
    
    # Saturn's axial tilt (relative to its orbital plane)
    saturn_axial_tilt_degrees = 26.73

    return RingData(inner_radius_m, outer_radius_m,
                    "assets/textures/saturnRingsTexture.png",
                    saturn_axial_tilt_degrees)