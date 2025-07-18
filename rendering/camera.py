# rendering/camera.py

import glfw
import numpy as np
import glm # pip install PyGLM
from config import CAMERA_SPEED, MOUSE_SENSITIVITY, WINDOW_WIDTH, WINDOW_HEIGHT

class Camera:
    def __init__(self, position):
        self.position = glm.vec3(position[0], position[1], position[2])
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.worldUp = glm.vec3(0.0, 1.0, 0.0) # Global up direction for calculating right vector

        self.yaw = -90.0 # Y-axis rotation (left/right). Start facing -Z.
        self.pitch = 0.0 # X-axis rotation (up/down)

        self.firstMouse = True
        self.lastMouseX = WINDOW_WIDTH / 2
        self.lastMouseY = WINDOW_HEIGHT / 2

        self._updateCameraVectors()

    def key_input_callback(self, key, action, mods):
        # Example: Toggling cursor on/off
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            if glfw.get_input_mode(glfw.glfwGetCurrentContext(), glfw.CURSOR) == glfw.CURSOR_DISABLED:
                glfw.set_input_mode(glfw.glfwGetCurrentContext(), glfw.CURSOR, glfw.CURSOR_NORMAL)
            else:
                glfw.set_input_mode(glfw.glfwGetCurrentContext(), glfw.CURSOR, glfw.CURSOR_DISABLED)

    def mouse_input_callback(self, xpos, ypos):
        # When mouse callback first called, set last positions
        if self.firstMouse:
            self.lastMouseX = xpos
            self.lastMouseY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastMouseX
        yoffset = self.lastMouseY - ypos # Reversed for OpenGL's Y-coordinates

        self.lastMouseX = xpos
        self.lastMouseY = ypos

        xoffset *= MOUSE_SENSITIVITY
        yoffset *= MOUSE_SENSITIVITY

        self.yaw += xoffset
        self.pitch += yoffset

        # Clamp pitch to avoid camera flipping
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self._updateCameraVectors()

    def processKeyboardInput(self, window, deltaTime):
        # Continuous key presses for movement
        speed = CAMERA_SPEED * deltaTime
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.position += self.front * speed
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.position -= self.front * speed
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.position -= self.right * speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.position += self.right * speed
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.position += self.worldUp * speed # Move directly up in world space
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.position -= self.worldUp * speed # Move directly down in world space

    def _updateCameraVectors(self):
        # Calculate new front vector based on yaw and pitch
        new_front = glm.vec3()
        new_front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        new_front.y = glm.sin(glm.radians(self.pitch))
        new_front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.front = glm.normalize(new_front)

        # Recalculate right and up vectors based on updated front
        self.right = glm.normalize(glm.cross(self.front, self.worldUp))
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def getViewMatrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def getProjectionMatrix(self, width, height):
        # Far plane set very large to accommodate solar system scale
        return glm.perspective(glm.radians(45.0), width / height, 0.1, 1_000_000_000.0) # Adjust far plane