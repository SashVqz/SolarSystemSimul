# main.py

import glfw
from OpenGL.GL import *
import numpy as np
import glm

from config import WINDOW_WIDTH, WINDOW_HEIGHT, SIMULATION_TIME_STEP, INITIAL_CAMERA_POSITION, \
                   POSITION_SCALE_FACTOR, RADIUS_SCALE_FACTOR, TIME_WARP
from physics.nBodySimulator import NBodySimulator
from rendering.windowManager import WindowManager
from rendering.camera import Camera
from rendering.shaderProgram import ShaderProgram
from entities.planetData import getSolarSystemBodies
from rendering.meshLoader import loadObjMesh # Now implicitly generates procedural sphere
from rendering.textureLoader import loadTexture
from rendering.ringRenderer import RingRenderer
from entities.ringData import getSaturnRingData

class SolarSystemApp:
    def __init__(self):
        # 1. Initialize GLFW and Window
        self.windowManager = WindowManager(WINDOW_WIDTH, WINDOW_HEIGHT, "Solar System Simulator")
        self.window = self.windowManager.getWindow()

        # Set up OpenGL viewport and initial settings
        glfw.make_context_current(self.window)
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND) # Enable blending for transparency (for rings)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Standard alpha blending
        glClearColor(0.0, 0.0, 0.0, 1.0) # Black background for space

        # Set up callbacks for input
        self.camera = Camera(INITIAL_CAMERA_POSITION)
        self.windowManager.registerKeyCallback(self.camera.key_input_callback)
        self.windowManager.registerMouseCallback(self.camera.mouse_input_callback)
        # Mouse cursor is set to disabled in camera for FPS controls:
        # glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # 2. Load Shaders
        self.shaderProgram = ShaderProgram("assets/shaders/vertexShader.glsl", "assets/shaders/fragmentShader.glsl")

        # Set up lighting uniforms that are constant (or depend on camera/sun)
        # These are initial values, you might need to fine-tune them
        self.shaderProgram.use()
        self.shaderProgram.setUniform1f("ambientStrength", 0.1) # Global ambient light
        self.shaderProgram.setUniform1f("diffuseStrength", 0.8) # How much diffuse light contributes
        self.shaderProgram.setUniform1f("specularStrength", 0.5) # How much specular highlight contributes
        self.shaderProgram.setUniform1f("shininess", 32.0) # Shininess of the material (e.g., plastic-like)
        self.shaderProgram.setUniformVec3("lightColor", glm.vec3(1.0, 1.0, 1.0)) # White light
        self.shaderProgram.unuse()

        # 3. Load Celestial Body Data
        self.celestialBodies = getSolarSystemBodies()
        self.simulator = NBodySimulator(self.celestialBodies, SIMULATION_TIME_STEP)

        # 4. Generate Mesh and Load Textures
        # We now generate a single sphere mesh procedurally to be reused for all bodies
        self.sphereMesh = loadObjMesh() # Call without path, or with dummy path if loadObjMesh checks it

        for body in self.celestialBodies:
            body.textureId = loadTexture(body.texturePath)

        # 5. Initialize Ring Renderer (for Saturn)
        self.ringRenderer = None
        saturn_body = next((body for body in self.celestialBodies if body.name == "Saturn"), None)
        if saturn_body:
            ring_data = getSaturnRingData()
            self.ringRenderer = RingRenderer(ring_data.innerRadius * RADIUS_SCALE_FACTOR,
                                             ring_data.outerRadius * RADIUS_SCALE_FACTOR,
                                             ring_data.texturePath,
                                             segments=128) # Higher segments for smoother rings
            # Pass ring tilt to ring renderer if needed, or handle in its render method
            self.saturn_ring_tilt = ring_data.tiltDegrees


        self.lastFrameTime = glfw.get_time()

    def run(self):
        while not glfw.window_should_close(self.window):
            currentFrameTime = glfw.get_time()
            deltaTime = currentFrameTime - self.lastFrameTime
            self.lastFrameTime = currentFrameTime

            # Process input
            self.windowManager.pollEvents() # Polls GLFW events
            self.camera.processKeyboardInput(self.window, deltaTime) # Process continuous key presses

            # Update simulation state
            self.simulator.update()

            # Render scene
            self._renderScene()

            # Swap buffers
            self.windowManager.swapBuffers()

    def _renderScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = self.camera.getProjectionMatrix(WINDOW_WIDTH, WINDOW_HEIGHT)
        view = self.camera.getViewMatrix()

        self.shaderProgram.use()
        self.shaderProgram.setUniformMat4("projection", projection)
        self.shaderProgram.setUniformMat4("view", view)
        self.shaderProgram.setUniformVec3("viewPos", self.camera.position)

        # Get Sun's position for lighting
        sun_body = next((body for body in self.celestialBodies if body.name == "Sun"), None)
        if sun_body:
            # Light direction is from fragment to sun. Assuming sun is source.
            # If Sun is at [0,0,0], light direction from any point is normalized(-FragPos).
            # If sun moves, it's normalize(sun_pos_scaled - FragPos_scaled).
            # For simplicity, assume distant light from the direction of sun.
            # Let's use the sun's actual scaled position as the light's position.
            scaled_sun_position = sun_body.position * POSITION_SCALE_FACTOR
            self.shaderProgram.setUniformVec3("lightDirection", glm.normalize(glm.vec3(scaled_sun_position[0], scaled_sun_position[1], scaled_sun_position[2]))) # Direction from origin to sun

            # For the Sun, it emits light, so it should appear fully lit
            # We can handle this by sending different uniforms or drawing it with a separate "unlit" shader.
            # For now, it will be lit by itself, which looks okay.

        # Render each celestial body
        for body in self.celestialBodies:
            scaled_position = body.position * POSITION_SCALE_FACTOR
            scaled_radius = body.radius * RADIUS_SCALE_FACTOR

            modelMatrix = glm.mat4(1.0)
            modelMatrix = glm.translate(modelMatrix, glm.vec3(scaled_position[0], scaled_position[1], scaled_position[2]))
            modelMatrix = glm.scale(modelMatrix, glm.vec3(scaled_radius, scaled_radius, scaled_radius))

            self.shaderProgram.setUniformMat4("model", modelMatrix)
            
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, body.textureId)

            self.sphereMesh.draw()

            # Render Saturn's rings
            if body.name == "Saturn" and self.ringRenderer:
                # RingRenderer will handle its own model matrix creation based on Saturn's position
                self.ringRenderer.render(self.shaderProgram, projection, view, modelMatrix)

        self.shaderProgram.unuse()
        glBindTexture(GL_TEXTURE_2D, 0) # Unbind texture after rendering

    def shutdown(self):
        if self.sphereMesh:
            self.sphereMesh.delete()
        if self.shaderProgram:
            self.shaderProgram.delete()
        if self.ringRenderer:
            self.ringRenderer.delete()
        for body in self.celestialBodies:
            if body.textureId:
                glDeleteTextures(1, [body.textureId])
        self.windowManager.terminate()

if __name__ == "__main__":
    app = SolarSystemApp()
    app.run()