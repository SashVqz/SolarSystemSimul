# rendering/meshLoader.py

from OpenGL.GL import *
import numpy as np
import glm
import os # For checking if OBJ path exists

class Mesh:
    def __init__(self):
        self.vao = None
        self.vbos = []
        self.ebo = None
        self.numElements = 0

    def load(self, vertices, texCoords, normals, indices):
        # Generar VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # VBO para posiciones de vértices (layout location 0)
        vbo_pos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_pos)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None) # Stride 0 if tightly packed
        glEnableVertexAttribArray(0)
        self.vbos.append(vbo_pos)

        # VBO para coordenadas de textura (layout location 1)
        vbo_tex = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_tex)
        glBufferData(GL_ARRAY_BUFFER, texCoords.nbytes, texCoords, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None) # Stride 0 if tightly packed
        glEnableVertexAttribArray(1)
        self.vbos.append(vbo_tex)

        # VBO para normales (layout location 2)
        vbo_norm = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_norm)
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None) # Stride 0 if tightly packed
        glEnableVertexAttribArray(2)
        self.vbos.append(vbo_norm)

        # EBO para índices
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        self.numElements = len(indices)

        # Desactivar VAO y VBOs
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.numElements, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def delete(self):
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            glDeleteBuffers(len(self.vbos), self.vbos)
            if self.ebo: glDeleteBuffers(1, [self.ebo])
            self.vao = None
            self.vbos = []
            self.ebo = None

def generate_sphere_data(radius=1.0, segments_x=64, segments_y=32):
    """
    Generates vertex positions, texture coordinates, normals, and indices for a sphere.
    segments_x: Number of segments around the equator (longitude).
    segments_y: Number of segments from pole to pole (latitude).
    """
    vertices = []
    normals = []
    tex_coords = []
    indices = []

    # Generate vertices, normals, and texture coordinates
    for y in range(segments_y + 1):
        pitch = np.pi / segments_y * y # Angle from top pole (0 to PI)
        for x in range(segments_x + 1):
            yaw = 2 * np.pi / segments_x * x # Angle around equator (0 to 2*PI)

            # Spherical coordinates to Cartesian
            # Map pitch to Y-axis, yaw to XZ plane
            px = radius * np.sin(pitch) * np.cos(yaw)
            py = radius * np.cos(pitch)
            pz = radius * np.sin(pitch) * np.sin(yaw)

            vertices.append([px, py, pz])

            # Normals are simply normalized vertex positions for a sphere centered at origin
            norm = glm.normalize(glm.vec3(px, py, pz))
            normals.append([norm.x, norm.y, norm.z])

            # Texture coordinates (equirectangular projection)
            u = float(x) / segments_x
            v = 1.0 - float(y) / segments_y # Invert V to match typical equirectangular maps (0 at top, 1 at bottom)
            tex_coords.append([u, v])

    # Generate indices for triangles
    for y in range(segments_y):
        for x in range(segments_x):
            # Current row, current column
            idx0 = y * (segments_x + 1) + x
            idx1 = idx0 + 1
            idx2 = (y + 1) * (segments_x + 1) + x
            idx3 = idx2 + 1

            # Two triangles forming a quad
            # Triangle 1: (Top-left, Bottom-left, Top-right)
            indices.append(idx0)
            indices.append(idx2)
            indices.append(idx1)

            # Triangle 2: (Top-right, Bottom-left, Bottom-right)
            indices.append(idx1)
            indices.append(idx2)
            indices.append(idx3)
            
    return (np.array(vertices, dtype=np.float32),
            np.array(tex_coords, dtype=np.float32),
            np.array(normals, dtype=np.float32),
            np.array(indices, dtype=np.uint32))


def loadObjMesh(filePath=None):
    """
    This function is now primarily used to generate a procedural sphere.
    The filePath argument is kept for compatibility but not strictly used for OBJ parsing.
    """
    from config import SPHERE_SEGMENTS_X, SPHERE_SEGMENTS_Y
    print(f"Generating procedural sphere with {SPHERE_SEGMENTS_X}x{SPHERE_SEGMENTS_Y} segments.")
    vertices, tex_coords, normals, indices = generate_sphere_data(
        radius=1.0, segments_x=SPHERE_SEGMENTS_X, segments_y=SPHERE_SEGMENTS_Y
    )
    
    mesh = Mesh()
    mesh.load(vertices, tex_coords, normals, indices)
    return mesh