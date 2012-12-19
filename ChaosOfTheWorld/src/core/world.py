'''
Created on 15.12.2012

@author: bernhard, eraldo
'''

from OpenGL.GL import *#@UnusedWildImport
from graphic import *#@UnusedWildImport
import random
import gameState

data_path = os.path.join("..", "..", "data")

NORTH, EAST, SOUTH, WEST = (0, 1), (1, 0), (0, -1), (-1, 0)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

def turnDirection(direction, turnDirection):
    index = DIRECTIONS.index(direction)
    index = (index + turnDirection) % len(DIRECTIONS)
    return DIRECTIONS[index]

def turnAngle(dirFrom, dirTo):
    indexFrom = DIRECTIONS.index(dirFrom)
    indexTo = DIRECTIONS.index(dirTo)
    return 90 * ((indexTo - indexFrom) % len(DIRECTIONS))

class World(object):
    INITIAL_MAP_SIZE = 100
    tiles = {}
    tileTypes = {}
    shaders = []
    
    def __init__(self, game, renderSize):
        self.game = game
        self.renderSize = renderSize
        self.init_shaders()
        self.load()
        
    def init_shaders(self):
        self.shader_min = 0
        self.shader_max = 8
        self.default_shader = 1
        self.shader = self.default_shader
        for n in range(9):
            self.shaders.append(Texture(os.path.join("shaders", "shader%s.png" % n)))
        self.shader_modifiers = []
        
    def updateShader(self):
        # mods: [modifier, life]
        self.shader = self.default_shader
        for mod in self.shader_modifiers:
            if mod[1] <= 0:
                self.shader_modifiers.remove(mod)
        for mod in self.shader_modifiers:
                mod[1] -= 1
                self.shader += mod[0]
        if self.shader < self.shader_min:
            self.shader = self.shader_min
        if self.shader > self.shader_max:
            self.shader = self.shader_max
        
    def draw(self):
        glPushMatrix()
        glRotate(turnAngle(NORTH, self.game.states[gameState.Running].player.direction), 0, 0, 1)
        
        # key: texture, value: [(posx, posy, Tile)]
        renderLists = {}
        
        for x in range(self.game.states[gameState.Running].player.position[0] - self.renderSize, self.game.states[gameState.Running].player.position[0] + self.renderSize + 1):
            for y in range(self.game.states[gameState.Running].player.position[1] - self.renderSize, self.game.states[gameState.Running].player.position[1] + self.renderSize + 1):
                if (x, y) in self.tiles:
                    xpos = x - self.game.states[gameState.Running].player.position[0]
                    ypos = y - self.game.states[gameState.Running].player.position[1]
                    tile = self.tiles[(x, y)]
                    texture = tile.tileType[tile.textureIndex]
                    if texture not in renderLists:
                        renderLists[texture] = []
                    renderLists[texture].append((xpos, ypos, tile))
                    
        for texture, renderList in renderLists.iteritems():
            texture.bind()
            for (xpos, ypos, tile) in renderList:
                glPushMatrix()
                glTranslatef(xpos, ypos, 0.0)
                tile.draw()
                glPopMatrix()
        
        # draw shader
        self.shaders[self.shader].bind()
        drawQuad(sideLength=17)
        

        glPopMatrix()
                
    def load(self):
        import csv

        direction_mapping = {
                             "N": NORTH,
                             "E": EAST,
                             "S": SOUTH,
                             "W": WEST,
                             }
        
        def getDirection(letter):
            if letter in direction_mapping.keys():
                return direction_mapping[letter]
            else:
                return random.choice(DIRECTIONS)
        
        def load_map():
            csv_map_file_path = os.path.join(data_path, "overworld-2.csv")
    
            tile_mapping = { # name-direction, speed, enterable
                1: ["grass-R", 1, True],
                2: ["forest-R", 1, True],
                3: ["water-R", 0, False],
                4: ["sand-R", 2, True],
                5: ["snow-R", 2, True],
                6: ["ice-R", 1, True],
                7: ["swamp-R", 3, True],
                8: ["road-R", 1, True],
                12: ["stone-R", 0, False],
                13: ["shelter-W", 0, False],
                14: ["shelter-E", 0, False],
                15: ["shelter-N", 0, False],
                16: ["shelter-S", 0, False],
            }
            
            
            for v in tile_mapping.itervalues():
                name, speed, enterable = v
                name =  name.split("-")[0]
                self.tileTypes[name] = TileType(name, [Texture(name+".png")], speed, enterable)
            
            self.rows = -1
            self.cols = -1
            with open(csv_map_file_path, 'rb') as csvfile:
                map_data = csv.reader(csvfile, delimiter=',')
                for y, row in enumerate(map_data):
                    self.rows += 1
                    self.cols = len(row)
                    for x, cell in enumerate(row):
                        if cell:
                            tile_mapping_key = int(cell)
                            type_name, direction_letter = tile_mapping[tile_mapping_key][0].split("-")
                            direction = getDirection(direction_letter)
                            tile_type = self.tileTypes[type_name]
                            self.tiles[(x, y)] = Tile(direction, tile_type, 0)
                        else:
                            pass # None -> new row
        
        load_map()

        def load_events():
            csv_events_file_path = os.path.join(data_path, "overworld-3-events.csv")
    
            from event import DayBreakEvent
            event_mapping = {
                            34: ["daybreak-R", DayBreakEvent]
                            }
    
            with open(csv_events_file_path, 'rb') as csvfile:
                events_data = csv.reader(csvfile, delimiter=',')
                for y, row in enumerate(events_data):
                    for x, cell in enumerate(row):
                        if cell:
                            event_mapping_key = int(cell)
                            if event_mapping_key in event_mapping.keys():
                                type_name, direction_letter = event_mapping[event_mapping_key][0].split("-")
                                direction = getDirection(direction_letter)
                                event_class = event_mapping[event_mapping_key][1]
                                self.tiles[(x, y)].events.append(event_class(self.game)) # TODO: add direction to event creation
                        else:
                            pass # None -> new row
        
        load_events()
        
        def load_items():
            csv_items_file_path = os.path.join(data_path, "overworld-3-items.csv")
    
            from item import LightSource
            item_mapping = {
                            34: ["flashlight-R", LightSource]
                            }
    
            with open(csv_items_file_path, 'rb') as csvfile:
                items_data = csv.reader(csvfile, delimiter=',')
                for y, row in enumerate(items_data):
                    for x, cell in enumerate(row):
                        if cell:
                            item_mapping_key = int(cell)
                            if item_mapping_key in item_mapping.keys():
                                name, direction_letter = item_mapping[item_mapping_key][0].split("-")
                                direction = getDirection(direction_letter)
                                item_class = item_mapping[item_mapping_key][1]
                                # for now.. spawn near shelters
                                near_x = -1
                                while near_x < 0 or near_x > self.cols: 
                                    near_x = x + random.randint(-10, 10)
                                near_y = -1
                                while near_y < 0 or near_y > self.rows: 
                                    near_y = y + random.randint(-10, 10)
                                
                                self.tiles[(near_x, near_y)].items.append(item_class(self.game, name)) # TODO: add direction to event creation
                        else:
                            pass # None -> new row
        
        load_items()

               
class Player(object):
    CRITICAL_BLOODLEVEL = 10
    def __init__(self, steps_max, days_max):
        self.direction = random.choice([NORTH, EAST, WEST, SOUTH])
        self.texture = Texture("player.png")
        self.position = (50, 40)
        self.steps = steps_max
        self.bloodPoints = 1
        self.collected_blood = 0 
        self.days = 0
        self.days_max =  days_max
        self.in_shelter = False
        self._alife = True
        self._hidden = False
        self.items = []
            
    def draw(self):
        if not self._hidden:
            self.texture.bind()
            drawQuad()
        
    def is_alife(self):
        if self.steps < 0 or self.bloodPoints < 0 or self.days > self.days_max:
            self._alife = False
            if self.steps < 0:
                self.steps = 0
        return self._alife
    
    def hide(self):
        self._hidden = True
    
    def unhide(self):
        self._hidden = False

    def feed(self, victims):
        self.collected_blood += victims
        self.bloodPoints += victims
    
    def exhaust(self):
        self.bloodPoints -= 1

    def die(self):
        self._alife = False
        
    
class TileType(object):   
    
    def __init__(self, name, textures, speed, enterable):
        self.textures = textures
        self.speed = speed
        self.enterable = enterable
        self.name = name
        
    def __getitem__(self,index):
        if index >= 0 and index < len(self.textures):
            return self.textures[index]
        elif len(self.textures):
            return self.textures[0]
        else:
            return None
    
class Tile(object):
    
    def __init__(self, direction, tileType, textureIndex):
        self.direction = direction
        self.tileType = tileType
        self.textureIndex = textureIndex
        self.events = []
        self.items = []
    
    def draw(self):
        glPushMatrix()
        rot = turnAngle(NORTH, self.direction)
        glRotatef(rot, 0, 0, 1)
        drawQuad()
        glPopMatrix()
        glPushMatrix()
        for event in self.events:
            event.draw()
        glPopMatrix()
        glPushMatrix()
        for item in self.items:
            item.draw()
        glPopMatrix()

        
    def canEnter(self, entity):
        return self.tileType.enterable
    
    def stepOnto(self, game):
        for event in self.events:
            event.trigger()
            if event.one_shot:
                del event
#        self.events = []
        for item in self.items:
            item.pickup()
            self.items.remove(item)
    
