'''
Created on 14.12.2012

@author: bernhard, eraldo
'''
from OpenGL.GL import * #@UnusedWildImport
from ctypes import *
from graphic import * #@UnusedWildImport
from hud import * #@UnusedWildImport
from world import * #@UnusedWildImport
import operator
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
        self.font = pygame.font.Font(None, 36)
        self.text = text
            
    def draw(self, screen, position, selected):
        
        glPushMatrix()
        glTranslatef(position[0], position[1], 0.0)
        rendered = self.font.render(self.text, 1, (255 * selected, 255, 255 * selected))
        texture = pygame.image.tostring(rendered, 'RGBA', True)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  
        
        aspect = rendered.get_width() * 1.0 / rendered.get_height()
        draw(aspect)
        
        glPopMatrix()
        
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
        self.options =  [MenuEntry("New Game", self.game.changeState, [Running]), 
                         MenuEntry("Options"),
                         MenuEntry("Exit", sys.exit)]
        if self.game.states[gameState.Running].initialized:
            self.options[0].text = "Continue" 
            self.options.insert(1, MenuEntry("New Game", self.restart, []))
            
    def restart(self):
        self.game.states[gameState.Running] = gameState.Running()
        self.game.changeState(Running)
        
    def update(self):
        pass
    
    def draw(self):
        drawPos = [0, self.game.coordinateSize / 2]
        for number, option in enumerate(self.options):
            option.draw(self.game.screen, drawPos, number != self.selection)
            drawPos[1] = drawPos[1] - self.game.coordinateSize / 4
            
class Running(GameState):
    steps_max = 100
    days_max = 100
    
    def __init__(self):
        self.player = Player(self.steps_max, self.days_max)
        self.world = None
        self.initialized = False

    def _menu(self):
        self.game.changeState(MainMenu)
        
    def _playerForward(self):
        if self.player.in_shelter:
            self.player.in_shelter = False
            self.player.unhide()
            self.hud.dayDisplay.switch_icon()
        if self.player.is_alife():
            newPosition = tuple(map(operator.add, self.player.position, self.player.direction))
            if newPosition in self.world.tiles:
                tile = self.world.tiles[newPosition]
                if tile.canEnter(self.player):
                    self.player.position = newPosition
                    self.player.steps -= tile.tileType.speed
                    tile.stepOnto(self.game)
            tile_type_name = self.world.tiles[newPosition].tileType.name
            if tile_type_name == "ice":
                self._playerForward()
            elif tile_type_name == "forest":
                self.world.shader_modifiers.append([-1, 1])
            else:
                pass
            
            self.world.updateShader()
                
        else: # died
            self.player.die()
            self.world.shader_modifier = []
            self.world.shader = 0
            self.hud.textBox.text = "You died a horrible death! ..You survived %s days and collected %s blood points." % (self.player.days, self.player.collected_blood)
        
    def _playerTurnLeft(self):
        if self.player.is_alife():
            self.player.direction = turnDirection(self.player.direction, -1)
        
    def _playerTurnRight(self):
        if self.player.is_alife():
            self.player.direction = turnDirection(self.player.direction, 1)
            
    def _playerBackward(self):
        if self.player.is_alife():
            self._playerTurnLeft()
            self._playerTurnLeft()        
            
    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        source = c_char_p(source)
        length = c_int(-1)
        glShaderSource(shader, 1, byref(source), byref(length))
        glCompileShader(shader)
        
        status = c_int()
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))
        if not status.value:
            self.print_log(shader)
            glDeleteShader(shader)
            raise ValueError, 'Shader compilation failed'
        return shader
 
    def compile_program(self, vertex_source, fragment_source):
        vertex_shader = None
        fragment_shader = None
        program = glCreateProgram()
     
        if vertex_source:
            vertex_shader = self.compile_shader(vertex_source, GL_VERTEX_SHADER)
            glAttachShader(program, vertex_shader)
        if fragment_source:
            fragment_shader = self.compile_shader(fragment_source, GL_FRAGMENT_SHADER)
            glAttachShader(program, fragment_shader)
     
        glLinkProgram(program)
     
        if vertex_shader:
            glDeleteShader(vertex_shader)
        if fragment_shader:
            glDeleteShader(fragment_shader)
     
        return program
                
    def print_log(self, shader):
        length = c_int()
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(length))
     
        if length.value > 0:
            log = create_string_buffer(length.value)
            glGetShaderInfoLog(shader, length, byref(length), log)
            print >> sys.stderr, log.value 
        
    def setup(self, game):
        super(Running, self).setup(game)
        game.keyUp[pygame.K_ESCAPE] = self._menu
        game.keyUp[pygame.K_UP] = self._playerForward
        game.keyUp[pygame.K_DOWN] = self._playerBackward
        game.keyUp[pygame.K_LEFT] = self._playerTurnLeft
        game.keyUp[pygame.K_RIGHT] = self._playerTurnRight
        if not self.initialized:
            self.world = World(self.game, game.coordinateSize)
            self.hud = Hud(self)            
            self.initialized = True   
        
    def update(self):
        pass
    
    def draw(self):
        glTranslate(-(self.game.aspect - 1.0) * self.game.coordinateSize + 0.5, 0.0, 0.0)
        self.world.draw()
        self.player.draw()
        glTranslate(self.game.coordinateSize, 0.0, 0.0)
        self.hud.draw()
        
        
