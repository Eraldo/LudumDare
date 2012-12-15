import os, pygame
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
   
SCREENWIDTH = 1920
SCREENHEIGHT = 1080
playerpos = (0, 0)
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(type, -1)
        
        self.rect.center = pos
        self.pos = pos
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
    def update(self):
        self.rect.centerx = (playerpos[0] - self.pos[0]) * self.rect.width + SCREENWIDTH / 2
        self.rect.centery = (playerpos[1] - self.pos[1]) * self.rect.height + SCREENHEIGHT / 2
    

    
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    
    
    
    tiles = {}
    
    for x in range(-20, 20):
        for y in range(-20, 20):
            tiles[(x, y)] = Tile((x, y), 'grass.png')
    
    
    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_h:
                for x in range(playerpos[0] - 10, playerpos[0] + 10):
                    for y in range(playerpos[1] - 10, playerpos[1] + 10):
                        tiles[(x, y)] = Tile((x, y), 'stone.png')
            elif event.type == KEYDOWN and event.key == K_g:
                for x in range(playerpos[0] - 10, playerpos[0] + 10):
                    for y in range(playerpos[1] - 10, playerpos[1] + 10):
                        tiles[(x, y)] = Tile((x, y), 'grass.png')
                
        renderTiles = pygame.sprite.Group()
        for x in range(playerpos[0] - 10, playerpos[0] + 10):
            for y in range(playerpos[1] - 10, playerpos[1] + 10):
                renderTiles.add(tiles[(x, y)])
                
        renderTiles.update()
        renderTiles.draw(screen)
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()