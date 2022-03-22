import pygame
# Destination display coordinates relative to the game's coordinate axis
class Destination():
	def __init__(self,Des,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.Des = Des
		self.des = pygame.transform.scale(self.Des,(self.width,self.height))
		self.des_rect = self.des.get_rect(topleft = (self.x,self.y))
	def draw(self,DISPLAYSURF,bg):
		self.des_rect.centerx += bg.scroll_x
		#pygame.draw.rect(DISPLAYSURF,(255,255,0),self.des_rect,2)
		DISPLAYSURF.blit(self.des,self.des_rect)
	def has_player(self,DISPLAYSURF,player):
		#print(self.des_rect.top)
		#print(self.des_rect.top + self.height/2)
		
		Rect = pygame.Rect( self.des_rect.left + 2*self.width/4, self.des_rect.top + self.height/2, self.width/5,self.height/2)
		#pygame.draw.rect(DISPLAYSURF,(255,255,255),Rect,2)
		#print('Rect.top',Rect.top)
		if pygame.Rect.colliderect(Rect,player.hero_rect_refer_game):
			
			player.Win = True

