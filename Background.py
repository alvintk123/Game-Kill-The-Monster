import pygame
# Background display coordinates relative to the game's coordinate axis
class Background():
    def __init__(self,img,x,y,WINDOWWIDTH,WINDOWHEIGHT):
        self.x = x
        self.y = y
        self.BG = img
        self.WINDOWWIDTH = WINDOWWIDTH
        self.BG = pygame.transform.scale(self.BG,(1000,WINDOWHEIGHT))
        # Speed of moving the screen
        self.scroll_x = 0
        # Speed of covering the screen
        self.cover_speed = 0
    def draw(self,DISPLAYSURF):
        DISPLAYSURF.blit(self.BG,(self.x,self.y))
    def move(self,player):
        self.scroll_x = 0
        # if player.hero_rect.left - self.x > 100 and -self.x + player.hero_rect.right < 1000 -100:
            
        #     if player.hero_rect.right > self.WINDOWWIDTH - self.x:
        #         self.scroll_x = - player.speed
        #         self.x += self.scroll_x
        #     if player.hero_rect.left < -self.x:
        #         self.scroll_x = player.speed 
        #         self.x += self.scroll_x
        # else:
        if player.hero_rect.right > self.WINDOWWIDTH - self.x:
            self.scroll_x = - player.speed
            self.x += self.scroll_x
        if player.hero_rect.left < -self.x :
            self.scroll_x = player.speed 
            self.x += self.scroll_x