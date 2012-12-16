'''
Created on 15.12.2012

@author: bernhard
'''
from OpenGL.GL import *#@UnusedWildImport
from graphic import *#@UnusedWildImport

#TODO: Split update and draw
class Hud(object):
    def __init__(self, owningState):
        self.owningState = owningState
        self.stepDisplay = StepDisplay(owningState, self)
        self.bloodPointDisplay = BloodDisplay(owningState, self)
        self.textBox = TextBox(owningState, self)
        self.inventory = Inventory(owningState, self)
        self.scale = 1.0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(0.5, self.owningState.game.coordinateSize - 0.5, 0.0)
        self.stepDisplay.draw()
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
        self.text = "This is my test sentence, there are many like it, but this one is mine!"
        font = "../../data/northwoodhigh.ttf" # TODO: change to relative path
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
    def __init__(self, owningState, hud,icon_file):
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
        glPushMatrix()
        draw(aspect, self.hud.scale)
        glPopMatrix()
        
    def draw(self):
        glPushMatrix()
        self.drawIcon()
        self.drawText()
        glPopMatrix()
        glTranslatef(0.0, -2.0, 0.0)

class StepDisplay(DisplayBase):
    def __init__(self, owningState, hud):
        super(StepDisplay, self).__init__(owningState, hud, "step_icon.png")
    
    def getValue(self):
        return self.owningState.player.steps
    
    def getMaxValue(self):
        return self.owningState.maxSteps
    
    def getTextColor(self):
        return (255 * (1 - self.valueRatio), 255 * self.valueRatio, 0)
    

        
class BloodDisplay(DisplayBase):
    def __init__(self, owningState, hud):
        super(BloodDisplay, self).__init__(owningState, hud, "blood_icon.png")
    
    def getValue(self):
        return self.owningState.player.bloodPoints
    
    def getMaxValue(self):
        return self.owningState.player.CRITICAL_BLOODLEVEL
    
    def getTextColor(self):
        return (255 * self.valueRatio, 0, 255 * (1 - self.valueRatio))
        

