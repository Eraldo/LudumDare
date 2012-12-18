'''
Created on 16.12.2012

@author: bernhard
'''

from OpenGL.GL import *#@UnusedWildImport
import pygame
import os
from baseGame import *

data_path = os.path.join("..", "..", "data")

def draw(aspectRatio, sideLength = 1.0):    
    halfLength = sideLength / 2.0
    glBegin (GL_QUADS)
    glTexCoord2f (0, 1);
    glVertex2f(-aspectRatio * halfLength, halfLength)
    glTexCoord2f (1, 1)
    glVertex2f(aspectRatio * halfLength, halfLength)
    glTexCoord2f (1, 0)
    glVertex2f(aspectRatio * halfLength, -halfLength)
    glTexCoord2f (0, 0)
    glVertex2f(-aspectRatio * halfLength, -halfLength)
    glEnd();

def drawQuad(sideLength = 1.0):
    halfLength = sideLength / 2.0
    glBegin (GL_QUADS)
    glTexCoord2f (0, 1);
    glVertex2f(-halfLength, halfLength)
    glTexCoord2f (1, 1)
    glVertex2f(halfLength, halfLength)
    glTexCoord2f (1, 0)
    glVertex2f(halfLength, -halfLength)
    glTexCoord2f (0, 0)
    glVertex2f(-halfLength, -halfLength)
    glEnd();
    
    
class Texture(object):
    currentTexture = None;
    
    def __init__(self, image):
        self.loadImage(image)
    
    def loadImage(self, image):
        textureSurface = pygame.image.load(os.path.join(data_path, image))
        self.textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        self.width = textureSurface.get_width()
        self.height = textureSurface.get_height()
 
    def bind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.textureData)
        Texture.currentTexture = self