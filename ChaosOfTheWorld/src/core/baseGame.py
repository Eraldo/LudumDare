'''
Created on 14.12.2012

@author: bernhard
'''

import pygame
import gameState
import sys

class BaseGame(object):
    run = True
    screen = None
    currentState = None
    
    states = {gameState.MainMenu: gameState.MainMenu(),
              gameState.Running: gameState.Running()}
    keyDown = {}
    keyUp = {}
    
    def __init__(self, startState):        
        self.setup()
        self.changeState(startState)
        
        while self.run:
            for event in pygame.event.get():
                action = None
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    action = self.keyDown.get(event.key)
                elif event.type == pygame.KEYUP:
                    action = self.keyUp.get(event.key)
                if action:
                    action()               
            self.currentState.update()
            self.currentState.draw()  
            pygame.display.flip()
            
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
    
    def changeState(self, state):
        self.keyDown.clear()
        self.keyUp.clear()
        self.states[state].setup(self)
        self.currentState = self.states[state]
            
            