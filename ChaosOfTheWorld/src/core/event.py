'''
Created on 15.12.2012

@author: bernhard
'''
import gameState
from graphic import *
from random import randint

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
        self.texture_consumed = Texture("welcome-steped.png")
        self.one_shot = False
        self.consumed = False
        self.victims = randint(1,4)
    
    def trigger(self):
        game = self.game.states[gameState.Running]
        game.player.in_shelter = True
        game.player.hide()
        game.player.steps = self.game.states[gameState.Running].steps_max
        game.hud.textBox.text = "You entered a shelter."
        game.world.shader_modifiers.append(+8)
        game.player.days += 1
        game.hud.dayDisplay.switch_icon()
        if game.player.days % 4 == 0: # every 4 days
            game.player.exhaust()
            game.hud.textBox.text += "You where exhausted and your blood level sank."
        
        if not self.consumed:
            self.consumed = True
            game.player.feed(self.victims)
            game.hud.textBox.text += " Lucky you.. you found %s innocent victims." % self.victims
            self.texture = self.texture_consumed
    
    def draw(self):
        oldTexture = Texture.currentTexture
        self.texture.bind()
        drawQuad()
        oldTexture.bind()
