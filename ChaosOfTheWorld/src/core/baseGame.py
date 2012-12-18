'''
Created on 14.12.2012

@author: bernhard, eraldo
'''

import pygame
import gameState
from OpenGL.GL import *#@UnusedWildImport
import sys, os

class BaseGame(object):
    coordinateSize = 16 / 2
    aspect = 1.0
    run = True
    screen = None
    currentState = None
    data_path = os.path.join("..", "..", "data")
    
    states = {gameState.MainMenu: gameState.MainMenu(),
              gameState.Running: gameState.Running()}
    keyDown = {}
    keyUp = {}
    
    def reshape(self):
        glViewport(0, 0, self.screen.get_width(), self.screen.get_height())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        self.aspect = self.screen.get_width() * 1.0 /  self.screen.get_height();
        glOrtho(-self.aspect * self.coordinateSize, self.aspect * self.coordinateSize, -self.coordinateSize , self.coordinateSize, -1, 1);
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
            self.clock.tick(16)
            self.handleEvents()
            self.currentState.update()
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslate(0.0, 0.5, 0.0)
            self.currentState.draw()
            pygame.display.flip()
            
    def setup(self):
        pygame.init()
        self.flags = pygame.OPENGL | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN
        self.modes = pygame.display.list_modes(0, self.flags)
        
        try:
            self.screen = pygame.display.set_mode(self.modes[0], self.flags)
        except:  # osx fullscreen fix
            self.screen = pygame.display.set_mode(self.modes[0], self.flags ^ pygame.FULLSCREEN)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.reshape()
        
        self.clock = pygame.time.Clock()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def changeState(self, state):
        self.keyDown.clear()
        self.keyUp.clear()
        self.states[state].setup(self)
        self.currentState = self.states[state]
            
            