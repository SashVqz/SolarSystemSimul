# rendering/windowManager.py

import glfw
from OpenGL.GL import *

class WindowManager:
    def __init__(self, width, height, title):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE) # Required for macOS

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)

        # Store mouse state for camera (initial position)
        self.lastMouseX = width / 2
        self.lastMouseY = height / 2
        self.firstMouse = True

        # Callbacks (registered by other modules like Camera)
        self.keyCallbacks = []
        self.mouseCallbacks = []
        self.scrollCallbacks = []

        # Set GLFW callbacks to internally dispatch to our registered callbacks
        glfw.set_key_callback(self.window, self._keyCallbackInternal)
        glfw.set_cursor_pos_callback(self.window, self._mouseCallbackInternal)
        glfw.set_scroll_callback(self.window, self._scrollCallbackInternal)

        # Enable V-Sync (Optional, helps prevent screen tearing)
        glfw.swap_interval(1)

    def getWindow(self):
        return self.window

    def _keyCallbackInternal(self, window, key, scancode, action, mods):
        # Dispatch to all registered key callbacks
        for callback in self.keyCallbacks:
            callback(key, action, mods)

    def _mouseCallbackInternal(self, window, xpos, ypos):
        # Dispatch to all registered mouse callbacks
        for callback in self.mouseCallbacks:
            callback(xpos, ypos)

    def _scrollCallbackInternal(self, window, xoffset, yoffset):
        # Dispatch to all registered scroll callbacks
        for callback in self.scrollCallbacks:
            callback(xoffset, yoffset)

    def registerKeyCallback(self, callback_func):
        self.keyCallbacks.append(callback_func)

    def registerMouseCallback(self, callback_func):
        self.mouseCallbacks.append(callback_func)

    def registerScrollCallback(self, callback_func):
        self.scrollCallbacks.append(callback_func)

    def shouldClose(self):
        return glfw.window_should_close(self.window)

    def swapBuffers(self):
        glfw.swap_buffers(self.window)

    def pollEvents(self):
        glfw.poll_events()

    def terminate(self):
        glfw.terminate()