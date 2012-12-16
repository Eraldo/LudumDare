'''
Created on 15.12.2012

@author: bernhard
'''
from OpenGL.GL import *#@UnusedWildImport
from graphic import *#@UnusedWildImport
import math
import random

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    #return -(math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0])) * 180.0 / math.pi
    return turnAngle(v1, v2)


NORTH, EAST, SOUTH, WEST = (0, 1), (1, 0), (0, -1), (-1, 0)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


def turnDirection(direction, turnDirection):
    index = DIRECTIONS.index(direction)
    index = (index + turnDirection) % len(DIRECTIONS)
    return DIRECTIONS[index]

def turnAngle(dirFrom, dirTo):
    indexFrom = DIRECTIONS.index(dirFrom)
    indexTo = DIRECTIONS.index(dirTo)
    return 90 * ((indexTo - indexFrom) % len(DIRECTIONS))

class World(object):
    INITIAL_MAP_SIZE = 100
    tiles = {}
    tileTypes = []
    
    def __init__(self, player, renderSize):
        self.player = player
        self.renderSize = renderSize
        self.load()
        
        
    def draw(self):
        glPushMatrix()
        glRotate(angle(NORTH, self.player.direction), 0, 0, 1)
        
        # key: texture, value: [(posx, posy, Tile)]
        renderLists = {}
        
        for x in range(self.player.position[0] - self.renderSize, self.player.position[0] + self.renderSize + 1):
            for y in range(self.player.position[1] - self.renderSize, self.player.position[1] + self.renderSize + 1):
                if (x, y) in self.tiles:
                    xpos = x - self.player.position[0]
                    ypos = y - self.player.position[1]
                    tile = self.tiles[(x, y)]
                    texture = tile.tileType[tile.textureIndex]
                    if texture not in renderLists:
                        renderLists[texture] = []
                    renderLists[texture].append((xpos, ypos, tile))
                    
        for texture, renderList in renderLists.iteritems():
            texture.bind()
            for (xpos, ypos, tile) in renderList:
                glPushMatrix()
                glTranslatef(xpos, ypos, 0.0)
                tile.draw()
                glPopMatrix()

        glPopMatrix()
    
    def load(self):
        self.tileTypes.append(TileType("Grass", [Texture("grass.png")], 1, True))
        self.tileTypes.append(TileType("Stone", [Texture("stone.png")], 1, True))
        
        for x in range(-self.INITIAL_MAP_SIZE, self.INITIAL_MAP_SIZE):
            for y in range(-self.INITIAL_MAP_SIZE, self.INITIAL_MAP_SIZE):
                tileDirection = random.choice(DIRECTIONS)
                tileType = random.choice(self.tileTypes)
                tileTexture = random.randint(0, len(tileType.textures))
                self.tiles[(x, y)] = Tile(tileDirection, tileType, tileTexture)
                
                
               
class Player(object):
    CRITICAL_BLOODLEVEL = 10
    def __init__(self, steps):
        self.direction = random.choice([NORTH, EAST, WEST, SOUTH])
        self.texture = Texture("player.png")
        self.position = (0, 0)
        self.steps = steps
        self.bloodPoints = 1
        
    def draw(self):
        self.texture.bind()
        drawQuad()
    
class TileType(object):   
    
    def __init__(self, name, textures, speed, enterable):
        self.textures = textures
        self.speed = speed
        self.enterable = enterable
        self.name = name
        
    def __getitem__(self,index):
        if index >= 0 and index < len(self.textures):
            return self.textures[index]
        elif len(self.textures):
            return self.textures[0]
        else:
            return None
    
class Tile(object):
    events = []
    
    def __init__(self, direction, tileType, textureIndex):
        self.direction = direction
        self.tileType = tileType
        self.textureIndex = textureIndex
    
    def draw(self):
        glPushMatrix()
        rot = angle(NORTH, self.direction)
        glRotatef(rot, 0, 0, 1)
        drawQuad()
        glPopMatrix()
    
    def canEnter(self, entity):
        return self.tileType.enterable
    
    def stepOnto(self, player):
        for event in self.events:
            event.trigger(player)
        self.events = []
    
