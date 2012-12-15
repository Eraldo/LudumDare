'''
Created on 14.12.2012

@author: bernhard
'''
import pygame
import sys
import world
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

class GameState(object):
    game = None
    
    def __init__(self):
        pass 
    
    def setup(self, game):
        self.game = game
        
    def update(self):
        pass
    
    def draw(self):
        pass
    

class MenuEntry(object):
    text = None
    font = None
    function = None
    
    args = None
    
    def __init__(self, text, function = None, args = []):
        self.args = args
        self.function = function
        if pygame.font:
            self.font = pygame.font.Font(None, 36)
            self.text = text
            
    def draw(self, screen, position, selected):
        
        glPushMatrix()
        glTranslatef(position[0], position[1], 0.0)
        rendered = self.font.render(self.text, 1, (255 * selected, 255, 255 * selected))
        texture = pygame.image.tostring(rendered, 'RGBA', True)
        
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  
        
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        aspect = rendered.get_width() * 1.0 / rendered.get_height()
        
        glBegin (GL_QUADS)
        glTexCoord2f (0, 1);
        glVertex2f(-aspect, 0.5)
        glTexCoord2f (1, 1)
        glVertex2f(aspect, 0.5)
        glTexCoord2f (1, 0)
        glVertex2f(aspect, -0.5)
        glTexCoord2f (0, 0)
        glVertex2f(-aspect, -0.5)
        glEnd();
        
        glPopMatrix()
        
        glDeleteTextures(textureId)
        
    def execute(self):
        if self.function:
            self.function(*self.args)
        

class MainMenu(GameState):
    
    options = []
    selection = 0
    font = None
    
    def _up(self):
        self.selection = self.selection - 1
        if self.selection < 0:
            self.selection = len(self.options) - 1
    def _down(self):
        self.selection = self.selection + 1
        if self.selection >= len(self.options):
            self.selection = 0
            
    def _escape(self):
        if self.selection == len(self.options) - 1:
            sys.exit()
        else:
            self.selection = len(self.options) - 1
            
    def _execute(self):
        self.options[self.selection].execute()
        
    def setup(self, game):
        super(MainMenu, self).setup(game)
        self.selection = 0
        game.keyUp[pygame.K_RETURN] = self._execute
        game.keyUp[pygame.K_UP] = self._up
        game.keyUp[pygame.K_DOWN] = self._down
        game.keyUp[pygame.K_ESCAPE] = self._escape
        self.options =  [MenuEntry("Start", self.game.changeState, [Running]), 
                         MenuEntry("Options"),
                         MenuEntry("Exit", sys.exit)]
        
    def update(self):
        pass
    
    def draw(self):
        drawPos = [0, self.game.coordinateSize / 2]
        for number, option in enumerate(self.options):
            option.draw(self.game.screen, drawPos, number != self.selection)
            drawPos[1] = drawPos[1] - self.game.coordinateSize / 2
            
class Running(GameState):
    
    def __init__(self):
        self.world = world.World()

    def _menu(self):
        self.game.changeState(MainMenu)
    
    def setup(self, game):
        super(Running, self).setup(game)
        game.keyUp[pygame.K_ESCAPE] = self._menu
        
    def update(self):
        pass
    
    def draw(self):
        pass