'''
Created on 14.12.2012

@author: bernhard
'''

import pygame
import gameState
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

class BaseGame(object):
    coordinateSize = 32 / 2
    
    run = True
    screen = None
    currentState = None
    
    states = {gameState.MainMenu: gameState.MainMenu(),
              gameState.Running: gameState.Running()}
    keyDown = {}
    keyUp = {}
    
    def reshape(self):
        glViewport(0, 0, self.screen.get_width(), self.screen.get_height())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspect = self.screen.get_width() * 1.0 /  self.screen.get_height();
        glOrtho(-aspect * self.coordinateSize, aspect * self.coordinateSize, -self.coordinateSize , self.coordinateSize, -1, 1);
        glMatrixMode(GL_MODELVIEW)
        
    def handleEvents(self):
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
    
    
    def __init__(self, startState):        
        self.setup()
        self.changeState(startState)
        
        while self.run:
            self.handleEvents()
            self.currentState.update()
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            self.currentState.draw()
            pygame.display.flip()
            
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.HWSURFACE | pygame.DOUBLEBUF, 16)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.reshape()
        
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def changeState(self, state):
        self.keyDown.clear()
        self.keyUp.clear()
        self.states[state].setup(self)
        self.currentState = self.states[state]
            
            