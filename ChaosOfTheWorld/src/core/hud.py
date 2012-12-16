'''
Created on 15.12.2012

@author: bernhard
'''
from OpenGL.GL import *#@UnusedWildImport
from graphic import *#@UnusedWildImport

#Todo Split update and draw
class Hud(object):
    
    def __init__(self, owningState):
        self.owningState = owningState
        self.stepDisplay = StepDisplay(owningState)
        self.bloodPointDisplay = BloodDisplay(owningState)
    
    def draw(self):
        glTranslatef(0.5, self.owningState.game.coordinateSize - 0.5, 0.0)
        self.stepDisplay.draw()
        self.bloodPointDisplay.draw()
        
class TextBox(object):
    def __init__(self, owningState):
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        
    def draw(self):
        rendered = self.font.render(self.text, 1, (255, 255, 255))
        texture = pygame.image.tostring(rendered, 'RGBA', True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  

class StepDisplay(object):
    def __init__(self, owningState):
        self.owningState = owningState
        self.font = pygame.font.Font(None, 36)
        self.icon = Texture("step_icon.png")
    
    def drawIcon(self):
        glTranslatef(0.5, -0.5, 0.0)
        self.icon.bind()
        drawQuad()
        glTranslatef(0.5, 0.5, 0.0)
        
    def drawStepText(self):
        stepRatio = self.owningState.player.steps * 1.0 / self.owningState.maxSteps
        if stepRatio < 0.0:
            stepRatio = 0.0
        if stepRatio > 1.0:
            stepRatio = 1.0 
        rendered = self.font.render("Steps: " + str(self.owningState.player.steps), 1, (255 * (1 - stepRatio), 255 * stepRatio, 0))
        texture = pygame.image.tostring(rendered, 'RGBA', True)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  

        aspect = rendered.get_width() * 1.0 / rendered.get_height()
        glTranslatef(aspect / 2.0, -0.5, 0.0)
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        draw(aspect)
        glPopMatrix()
        
    def draw(self):
        glPushMatrix()
        self.drawIcon()
        self.drawStepText()
        glPopMatrix()
        glTranslatef(0.0, -1.0, 0.0)
        
class BloodDisplay(object):
    def __init__(self, owningState):
        self.owningState = owningState
        self.font = pygame.font.Font(None, 36)
        self.icon = Texture("blood_icon.png")
    
    def drawIcon(self):
        glTranslatef(0.5, -0.5, 0.0)
        self.icon.bind()
        drawQuad()
        glTranslatef(0.5, 0.5, 0.0)
        
    def drawBloodText(self):
        bloodRatio = self.owningState.player.bloodPoints / 20.0
        if bloodRatio < 0.0:
            bloodRatio = 0.0
        if bloodRatio > 1.0:
            bloodRatio = 1.0
        rendered = self.font.render("Blood: " + str(self.owningState.player.bloodPoints), 1, (255 * bloodRatio, 0, 255 * (1 - bloodRatio)))
        texture = pygame.image.tostring(rendered, 'RGBA', True)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rendered.get_width(), rendered.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )  

        aspect = rendered.get_width() * 1.0 / rendered.get_height()
        glTranslatef(aspect / 2.0, -0.5, 0.0)
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        draw(aspect)
        glPopMatrix()
        
    def draw(self):
        glPushMatrix()
        self.drawIcon()
        self.drawBloodText()
        glPopMatrix()
        glTranslatef(0.0, -1.0, 0.0)

