# rendering/ringRenderer.py

from OpenGL.GL import *
import numpy as np
import glm
from rendering.textureLoader import loadTexture

class RingRenderer:
    def __init__(self, innerRadius, outerRadius, texturePath, segments=128):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.texturePath = texturePath
        self.textureId = loadTexture(texturePath)
        self.numSegments = segments
        self.vao = None
        self.vbos = []
        self.ebo = None
        self.numElements = 0
        self._setupMesh()

    def _setupMesh(self):
        vertices = []
        texCoords = []
        indices = []

        # Generate points for inner and outer circles
        for i in range(self.numSegments + 1):
            angle = 2.0 * np.pi * i / self.numSegments
            x_outer = self.outerRadius * np.cos(angle)
            y_outer = self.outerRadius * np.sin(angle)
            x_inner = self.innerRadius * np.cos(angle)
            y_inner = self.innerRadius * np.sin(angle)

            # Outer ring vertex
            vertices.extend([x_outer, 0.0, y_outer]) # Lay flat on XZ plane
            texCoords.extend([float(i) / self.numSegments, 1.0]) # U = angle, V = outer edge
            
            # Inner ring vertex
            vertices.extend([x_inner, 0.0, y_inner]) # Lay flat on XZ plane
            texCoords.extend([float(i) / self.numSegments, 0.0]) # U = angle, V = inner edge

        # Generate indices for triangles
        for i in range(self.numSegments):
            outer_idx1 = 2 * i
            inner_idx1 = 2 * i + 1
            outer_idx2 = 2 * (i + 1)
            inner_idx2 = 2 * (i + 1) + 1

            # Triangle 1: (outer_idx1, inner_idx1, inner_idx2)
            indices.extend([outer_idx1, inner_idx1, inner_idx2])
            # Triangle 2: (outer_idx1, inner_idx2, outer_idx2)
            indices.extend([outer_idx1, inner_idx2, outer_idx2])
            
        self.numElements = len(indices)

        # Normals for a flat ring on the XZ plane, pointing up (+Y)
        # All normals are simply (0, 1, 0)
        normals = np.array([[0.0, 1.0, 0.0]] * (len(vertices) // 3), dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Positions (location 0)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(vertices, dtype=np.float32).nbytes, np.array(vertices, dtype=np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        self.vbos.append(self.vbo)

        # Texture Coordinates (location 1)
        self.vbo_tex = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_tex)
        glBufferData(GL_ARRAY_BUFFER, np.array(texCoords, dtype=np.float32).nbytes, np.array(texCoords, dtype=np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        self.vbos.append(self.vbo_tex)

        # Normals (location 2)
        self.vbo_norm = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_norm)
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)
        self.vbos.append(self.vbo_norm)

        # Indices (EBO)
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array(indices, dtype=np.uint32).nbytes, np.array(indices, dtype=np.uint32), GL_STATIC_DRAW)

        glBindVertexArray(0)

    def render(self, shaderProgram, projectionMatrix, viewMatrix, saturnModelMatrix):
        shaderProgram.use() # Ensure shader is active for rings

        # The rings are flat on the XZ plane (Y=0) in their local space.
        # Saturn's axial tilt is applied by rotating around the X-axis.
        ringModelMatrix = glm.translate(glm.mat4(1.0), glm.vec3(saturnModelMatrix[3])) # Start with Saturn's position
        ringModelMatrix = glm.rotate(ringModelMatrix, glm.radians(-26.73), glm.vec3(1.0, 0.0, 0.0)) # Tilt of Saturn's axis

        shaderProgram.setUniformMat4("model", ringModelMatrix)
        shaderProgram.setUniform1i("ourTexture", 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureId)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.numElements, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0) # Unbind texture

    def delete(self):
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            glDeleteBuffers(len(self.vbos), self.vbos)
            if self.ebo: glDeleteBuffers(1, [self.ebo])
            glDeleteTextures(1, [self.textureId])
            self.vao = None
            self.vbos = []
            self.ebo = None
            self.textureId = None