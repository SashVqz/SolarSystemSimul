# rendering/shaderProgram.py

from OpenGL.GL import *
import numpy as np
import glm

class ShaderProgram:
    def __init__(self, vertexShaderPath, fragmentShaderPath):
        self.program = self._createShaderProgram(vertexShaderPath, fragmentShaderPath)

    def _createShaderProgram(self, vertexShaderPath, fragmentShaderPath):
        vertex_shader_code = self._loadShader(vertexShaderPath)
        fragment_shader_code = self._loadShader(fragmentShaderPath)

        vertex_shader = self._compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragment_shader = self._compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)

        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            info = glGetProgramInfoLog(program)
            glDeleteProgram(program)
            glDeleteShader(vertex_shader)
            glDeleteShader(fragment_shader)
            raise RuntimeError(f"Error linking shader program:\n{info.decode('utf-8')}")

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        return program

    def _loadShader(self, path):
        with open(path, 'r') as f:
            return f.read()

    def _compileShader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            info = glGetShaderInfoLog(shader)
            glDeleteShader(shader)
            raise RuntimeError(f"Error compiling {shader_type} shader:\n{info.decode('utf-8')}")
        return shader

    def use(self):
        glUseProgram(self.program)

    def unuse(self):
        glUseProgram(0)

    def setUniformMat4(self, name, matrix):
        location = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(matrix))

    def setUniformVec3(self, name, vector):
        location = glGetUniformLocation(self.program, name)
        glUniform3fv(location, 1, glm.value_ptr(vector))

    def setUniform1i(self, name, value):
        location = glGetUniformLocation(self.program, name)
        glUniform1i(location, value)

    def setUniform1f(self, name, value):
        location = glGetUniformLocation(self.program, name)
        glUniform1f(location, value)

    def delete(self):
        glDeleteProgram(self.program)