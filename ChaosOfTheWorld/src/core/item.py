'''
Created on 15.12.2012

@author: bernhard
'''

class Item(object):
    def __init__(self):
        self.timeToLive = -1
        self.activated = False
        self.name = "Invalid"
        self.icon = None
        self.category = None
    
    def trigger(self, player):
        pass 
    