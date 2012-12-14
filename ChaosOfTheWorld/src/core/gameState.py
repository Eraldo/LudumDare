'''
Created on 14.12.2012

@author: bernhard
'''

class GameState(object):
    game = None
    
    def __init__(self):
        pass 
    
    def setup(self, game):
        self.game = game
        return
        
    def update(self):
        return
    
    def draw(self):
        return