'''
Created on 15.12.2012

@author: bernhard
'''
import gameState
from graphic import *

class Event(object):
    def __init__(self, game):
        self.game = game
        self.name = None
        self.texture = None
        self.one_shot = True
    
    def trigger(self):
        pass
    
    def draw(self):
        pass

class DayBreakEvent(Event):
    def __init__(self, game):
        super(DayBreakEvent, self).__init__(game)
        self.name = "daybreak"
        self.texture = Texture("welcome.png")
#        self.texture = texture # TODO: define
    
    def trigger(self):
        self.game.states[gameState.Running].player.bloodPoints += 1
        self.game.states[gameState.Running].player.steps = self.game.states[gameState.Running].maxSteps
        self.game.states[gameState.Running].hud.textBox.text = "You entered a shelter."
        # TODO: remove alpha blending
        # TODO: make player invisible
        # TODO: display notification of shelter
        # TODO: increase the bloodpoints
    
    def draw(self):
        self.texture.bind()
        drawQuad()