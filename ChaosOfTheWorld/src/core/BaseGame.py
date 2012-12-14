'''
Created on 14.12.2012

@author: bernhard
'''
import abc


class BaseGame:
    run = True
    keymap = {}
    
    def __init__(self):
        self.setup()
        
        while self.run:
            self.update()
            self.draw()
            
    @abc.abstractmethod
    def setup(self):
        pass
    
    @abc.abstractmethod
    def update(self):
        pass
    
    @abc.abstractmethod
    def draw(self):
        pass