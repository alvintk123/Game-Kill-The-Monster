
import pygame

# object display coordinates relative to the game's coordinate axis
class object(pygame.sprite.Sprite):
    def __init__(self,img,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.y_init = y
        self.width = int(width/2)
        self.height = int(height/2)
        self.image = pygame.transform.scale(img,(width,height))
        self.rect = self.image.get_rect(center = (x,y))

    def update(self,bg):
        self.rect.centerx += bg.scroll_x
        # fix after bounced on top screen
        self.rect.centery = self.y_init + bg.y