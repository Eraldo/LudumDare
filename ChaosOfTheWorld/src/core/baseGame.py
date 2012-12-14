'''
Created on 14.12.2012

@author: bernhard
'''

import pygame

class BaseGame(object):
    run = True
    screen = None
    currentState = None
    keymap = {}
    
    def __init__(self, startState):        
        self.setup()
        self.changeState(startState)
        
        while self.run:
            self.currentState.update()
            self.currentState.draw()  
            
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
    
    def changeState(self, state):
        state.setup(self)
        self.currentState = state
            
            