'''
Created on 16.12.2012

@author: bernhard
'''

from OpenGL.GL import *#@UnusedWildImport
import pygame 

def draw(aspectRatio):
    glBegin (GL_QUADS)
    glTexCoord2f (0, 1);
    glVertex2f(-aspectRatio, 0.5)
    glTexCoord2f (1, 1)
    glVertex2f(aspectRatio, 0.5)
    glTexCoord2f (1, 0)
    glVertex2f(aspectRatio, -0.5)
    glTexCoord2f (0, 0)
    glVertex2f(-aspectRatio, -0.5)
    glEnd();

def drawQuad():
    glBegin (GL_QUADS)
    glTexCoord2f (0, 1);
    glVertex2f(-0.5, 0.5)
    glTexCoord2f (1, 1)
    glVertex2f(0.5, 0.5)
    glTexCoord2f (1, 0)
    glVertex2f(0.5, -0.5)
    glTexCoord2f (0, 0)
    glVertex2f(-0.5, -0.5)
    glEnd();
    
    
class Texture(object):
    def __init__(self, image):
        self.loadImage(image)
    
    def loadImage(self, image):
        textureSurface = pygame.image.load("../../data/" + image)
        self.textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        self.width = textureSurface.get_width()
        self.height = textureSurface.get_height()
 
    def bind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.textureData)