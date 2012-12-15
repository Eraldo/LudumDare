'''
Created on 14.12.2012

@author: bernhard
'''
from OpenGL.GL import *#@UnusedWildImport
from core.world import Player, turnDirection, World
import operator
import pygame
import sys


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
        
        textureId = 0#glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  
        
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
        
        #glDeleteTextures(textureId)
        
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
        self.player = Player()
        self.world = None
        self.initialized = False

    def _menu(self):
        self.game.changeState(MainMenu)
        
    def _playerForward(self):
        newPosition = tuple(map(operator.add, self.player.position, self.player.direction))
        if newPosition in self.world.tiles:
            tile = self.world.tiles[newPosition]
            if tile.canEnter(self.player):
                tile.stepOnto(self.player)
                self.player.position = newPosition
        
    def _playerTurnLeft(self):
        self.player.direction = turnDirection(self.player.direction, -1)
        sys.stdout.flush()
        
    def _playerTurnRight(self):
        self.player.direction = turnDirection(self.player.direction, 1)
        sys.stdout.flush()
        
    def setup(self, game):
        super(Running, self).setup(game)
        game.keyUp[pygame.K_ESCAPE] = self._menu
        game.keyUp[pygame.K_UP] = self._playerForward
        game.keyUp[pygame.K_LEFT] = self._playerTurnLeft
        game.keyUp[pygame.K_RIGHT] = self._playerTurnRight
        if not self.initialized:
            
            self.world = World(self.player, game.coordinateSize)
            
            
            self.initialized = True
        
    def update(self):
        pass
    
    def draw(self):
        glTranslate(-(self.game.aspect - 1.0) * self.game.coordinateSize + 0.5, 0.0, 0.0)
        self.world.draw()
        self.player.draw()