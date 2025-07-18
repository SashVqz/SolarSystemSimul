# rendering/textureLoader.py

from OpenGL.GL import *
from PIL import Image # Import Pillow
import numpy as np

def loadTexture(filePath):
    """
    Loads an image file using Pillow and converts it into an OpenGL texture.
    Returns the OpenGL texture ID.
    """
    try:
        # Load image with Pillow
        img = Image.open(filePath)
        
        # Convert image to RGBA format if it's not already
        # This handles transparency (alpha channel) for PNGs like Saturn's rings.
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get image data as bytes
        img_data = np.array(list(img.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # Set texture filtering parameters (mipmaps for minification)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Upload the image data to the GPU
        # Pillow's data is already top-left origin, so no need to flip `img_data` itself.
        # OpenGL expects GL_RGBA for data that includes alpha, GL_UNSIGNED_BYTE for 8-bit per channel.
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D) # Generate mipmaps

        glBindTexture(GL_TEXTURE_2D, 0) # Unbind the texture

        print(f"Successfully loaded texture: {filePath}")
        return texture_id

    except Exception as e:
        print(f"Error loading texture {filePath}: {e}")
        return 0