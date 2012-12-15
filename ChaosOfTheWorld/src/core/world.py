'''
Created on 15.12.2012

@author: bernhard
'''
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

NORTH, EAST, WEST, SOUTH = (0.0, 1.0), (1.0, 0.0), (-1.0, 0.0), (0.0, -1.0)

class World(object):
    tiles = {}
    def __init__(self):
        pass
    
class TileTexture(object):
    def __init__(self, image):
        self.loadImage(image)
    
    def loadImage(self, image):
        textureSurface = pygame.image.load("data/" + image)
        self.textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        self.width = textureSurface.get_width()
        self.height = textureSurface.get_height()
 
    def bind(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.textureData)
        return texture
    
    
class Tile(object):
    
    
    def __init__(self, direction):
        self.direction = direction
        