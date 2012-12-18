'''
Created on 15.12.2012

@author: bernhard, eraldo
'''

import gameState
from graphic import *
import os

class Item(object):
    def __init__(self, game):
        self.game = game.states[gameState.Running]
        self.name = None
        self.icon = None
        self.timeToLive = -1
        self.activated = False
        self.category = None
    
    def trigger(self):
        pass

    def draw(self):
        pass

class LightSource(Item):
    
    def __init__(self, game, name=None, timeToLive=100):
        super(LightSource, self).__init__(game)
        self.name = name
        self.icon = Texture(os.path.join("items", name + ".png"))
        self.timeToLive = timeToLive
        self.category = "LightSource"
        
    def pickup(self):
        self.game.player.items.append(self)
        self.game.hud.textBox.text = "You picked up a %s." % self.name
        self.game.world.shader_modifiers.append([+1, self.timeToLive])  
        
    def trigger(self):
        print(self.name + " got triggered")

    def draw(self):
        oldTexture = Texture.currentTexture
        self.icon.bind()
        drawQuad()
        oldTexture.bind()