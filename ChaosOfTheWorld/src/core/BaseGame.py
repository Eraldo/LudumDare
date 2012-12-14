'''
Created on 14.12.2012

@author: bernhard
'''

import pygame

class BaseGame:
    run = True
    screen = None
    currentState = None
    keymap = {}
    
    def __init__(self, startState):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        
        self.setup()
        self.changeState(startState)
        
        while self.run:
            self.update()
            self.draw()
            
    def setup(self):
        pass
    
    def update(self):
        self.currentState.update()
    
    def draw(self):
        self.currentState.draw()
    
    def changeState(self, state):
        state.setup(self)
        self.currentState = state
            
            