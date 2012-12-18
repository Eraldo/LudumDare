'''
Created on 15.12.2012

@author: bernhard
'''
from OpenGL.GL import *#@UnusedWildImport
from graphic import *#@UnusedWildImport

data_path = os.path.join("..", "..", "data")

#TODO: Split update and draw
class Hud(object):
    def __init__(self, owningState):
        self.owningState = owningState
        self.stepDisplay = StepDisplay(owningState, self)
        self.dayDisplay = DayDisplay(owningState, self)
        self.bloodPointDisplay = BloodDisplay(owningState, self)
        self.textBox = TextBox(owningState, self)
        self.inventory = Inventory(owningState, self)
        self.scale = 1.0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(0.5, self.owningState.game.coordinateSize - 0.5, 0.0)
        self.stepDisplay.draw()
        self.dayDisplay.draw()
        self.bloodPointDisplay.draw()
        self.textBox.draw()
        glPopMatrix()
        glTranslatef(0.5, -self.owningState.game.coordinateSize - 0.5, 0.0)
        
        
class Inventory(object):
    def __init__(self, owningState, hud):
        self.owningState = owningState
        self.hud = hud
        
    def draw(self):
        pass

class TextBox(object):
    def __init__(self, owningState, hud):
        self.text = """
        It is night.. 
        You feel dizzy..
        You should try to find shelters before day breaks!
        Controlls:
        UP: move forward
        RIGHT: turn right 
        LEFT: turn left
        DOWN: turn around
        ESC: Menu
        """
        font = os.path.join(data_path, "northwoodhigh.ttf")
        self.font = pygame.font.Font(font, 28)
        self.hud = hud
        self.owningState = owningState
        
    def draw(self):
        lineSpace = self.owningState.game.coordinateSize * (self.owningState.game.aspect - 1.0) * 2.0 - 2.0
        usedSpace = 0.0
        glTranslatef(0.5, -1.0, 0.0)
        glPushMatrix()
        for word in self.text.split(" "):
            rendered = self.font.render(word, 1, (255, 255, 255))
            texture = pygame.image.tostring(rendered, 'RGBA', True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
            
            aspect = rendered.get_width() * 1.0 / rendered.get_height()
            
            if lineSpace - usedSpace < aspect * self.hud.scale / 2.0:
                glPopMatrix()
                glTranslatef(0.0, -self.hud.scale / 1.25, 0.0)
                glPushMatrix()
                usedSpace = 0.0
                
            glTranslatef(self.hud.scale * aspect / 4.0, 0.0, 0.0)
            draw(aspect, self.hud.scale / 2.0)
            glTranslatef(self.hud.scale * aspect / 4.0 + 0.1, 0.0, 0.0)
            usedSpace = usedSpace + aspect * self.hud.scale / 2.0 + 0.1
        glPopMatrix()

class DisplayBase(object):
    def __init__(self, owningState, hud, icon_file):
        self.owningState = owningState
        self.font = pygame.font.Font(None, 36)
        self.icon = Texture(icon_file)
        self.valueRatio = 0.0
        self.hud = hud
    
    def drawIcon(self):
        glTranslatef(1.0, -1.0, 0.0)
        self.icon.bind()
        drawQuad(2.0)
        glTranslatef(1.0, 1.0, 0.0)
        
    def drawText(self):
        self.valueRatio = self.getValue() * 1.0 / self.getMaxValue()
        if self.valueRatio < 0.0:
            self.valueRatio = 0.0
        if self.valueRatio > 1.0:
            self.valueRatio = 1.0
            
        rendered = self.font.render(str(self.getValue()).rjust(5, ' '), 1, self.getTextColor())
        
        texture = pygame.image.tostring(rendered, 'RGBA', True)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  

        aspect = rendered.get_width() * 1.0 / rendered.get_height()
        freeSpace = self.owningState.game.coordinateSize * (self.owningState.game.aspect - 1.0) - 0.75
       
        scale = freeSpace / aspect
        if scale < self.hud.scale:
            self.hud.scale = scale
        
        glTranslatef(self.hud.scale * aspect / 2.0, -1.0, 0.0)
        draw(aspect, self.hud.scale)
        
    def draw(self):
        glPushMatrix()
        self.drawIcon()
        self.drawText()
        glPopMatrix()
        glTranslatef(0.0, -2.0, 0.0)
        

class StepDisplay(DisplayBase):
    def __init__(self, owningState, hud):
        super(StepDisplay, self).__init__(owningState, hud, "steps_icon.png")
    
    def getValue(self):
        return self.owningState.player.steps
    
    def getMaxValue(self):
        return self.owningState.steps_max
    
    def getTextColor(self):
        return (255 * (1 - self.valueRatio), 255 * self.valueRatio, 0)
    
    
class DayDisplay(DisplayBase):
    def __init__(self, owningState, hud):
        self.icon_day = Texture("day_icon.png")
        self.icon_night = Texture("night_icon.png")
        super(DayDisplay, self).__init__(owningState, hud, "days_icon.png")
        self.switch_icon()
    
    def getValue(self):
        return self.owningState.player.days
    
    def getMaxValue(self):
        return self.owningState.days_max
            
    def getTextColor(self):
        return (255 * self.valueRatio, 255 * (1 - self.valueRatio), 0)
    
    def switch_icon(self):
        if self.icon == self.icon_night:
            self.icon = self.icon_day
        else:
            self.icon = self.icon_night     
    
        
class BloodDisplay(DisplayBase):
    def __init__(self, owningState, hud):
        super(BloodDisplay, self).__init__(owningState, hud, "blood_icon.png")
    
    def getValue(self):
        return self.owningState.player.bloodPoints
    
    def getMaxValue(self):
        return self.owningState.player.CRITICAL_BLOODLEVEL
    
    def getTextColor(self):
        return (255 * self.valueRatio, 0, 255 * (1 - self.valueRatio))
        

