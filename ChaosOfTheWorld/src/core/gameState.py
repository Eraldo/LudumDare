'''
Created on 14.12.2012

@author: bernhard
'''
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
        rendered = self.font.render(self.text, 1, (255 * selected, 255, 255 * selected))
        screen.blit(rendered, rendered.get_rect(centerx = position[0], centery = position[1]))
        
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
        drawPos = [self.game.screen.get_width() / 2, self.game.screen.get_height() / 5]
        for number, option in enumerate(self.options):
            
            option.draw(self.game.screen, drawPos, number != self.selection)
            drawPos[1] = drawPos[1] + self.game.screen.get_height() / 5
            

    
    
class Running(GameState):
    
    def setup(self, game):
        super(Running, self).setup(game)
        
    def update(self):
        pass
    
    def draw(self):
        pass