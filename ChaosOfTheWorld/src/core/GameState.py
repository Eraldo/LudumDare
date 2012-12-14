'''
Created on 14.12.2012

@author: bernhard
'''
import abc

class GameState(object):
    initialized = False
    
    def __init__(self):
        pass
        
    @abc.abstractmethod
    def update(self):
        return
    
    def draw(self):
        return
    