'''
Created on 15.12.2012

@author: bernhard
'''
import gameState

class Event(object):
    def __init__(self):
        self.name = None
        self.texture = None
        self.one_shot = True
    
    def trigger(self, game):
        pass
    
    def draw(self):
        pass

class DayBreakEvent(Event):
    def __init__(self):
        super(DayBreakEvent, self).__init__()
        self.name = "daybreak"
#        self.texture = texture # TODO: define
    
    def trigger(self, game):
        game.states[gameState.Running].player.bloodPoints += 1
        game.states[gameState.Running].player.steps += 100
        # TODO: remove alpha blending
        # TODO: make player invisible
        # TODO: display notification of shelter
        # TODO: increase the bloodpoints
    
    def draw(self):
        pass        