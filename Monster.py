import pygame
from Object import object
# monster display coordinates relative to the game's coordinate axis
class monster(pygame.sprite.Sprite):
    def __init__(self,animation_list,x,y,width,height,direction,speed,bound_left,bound_right):
        self.direction, self.speed = direction,speed
        self.bound_left, self.bound_right = bound_left, bound_right
        self.height, self.width = height , width
        # Time init
        self.time_init = pygame.time.get_ticks()
        # Frame
        self.frame = 0
        # Type of action 
        self.type_action = 'Move'
        # List animation 
        self.list_animation = animation_list
        self.image = pygame.transform.scale(self.list_animation[self.type_action][self.frame],(self.width,self.height))
        self.rect = self.image.get_rect(center = (x,y))

        pygame.sprite.Sprite.__init__(self)
    def update(self,bg,player,monster_group):
        self.move(bg)
        self.update_draw()
        # Interact with player
        self.interact(player)

    def update_draw(self):
        cooldown = 50 #ms
        time_now = pygame.time.get_ticks()
        self.image = self.list_animation[self.type_action][self.frame]
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image,True,False)
        if time_now - self.time_init > cooldown:
            self.frame += 1
            self.time_init = time_now
            if self.frame >= len(self.list_animation[self.type_action]):
                self.frame = 0            
    def move(self,bg):        
        # Change boundary when scroll
        self.bound_left += bg.scroll_x
        self.bound_right += bg.scroll_x
        # Move monster as default
        if self.direction == 'left':
            self.rect.centerx -= self.speed
            if self.rect.left  <= self.bound_left:
                self.rect.left = self.bound_left
                self.direction = 'right'
        if self.direction == 'right':
            self.rect.centerx += self.speed
            if self.rect.right  >= self.bound_right:
                self.rect.right = self.bound_right
                self.direction = 'left'
        # Change position when scroll
        self.rect.centerx += bg.scroll_x
    def interact(self,player):
        
        # compare with the game's reference coordinate axis of player
        if pygame.Rect.colliderect(self.rect,player.hero_rect_refer_game) and not player.Back_TakingDame:
            print('touch')
            if player.type_action == 'Attack':
                if player.hero_rect_refer_game.centerx > (self.rect.centerx) and player.direction == 'left':
                    self.kill()
                    player.score += 1
                elif player.hero_rect_refer_game.centerx < (self.rect.centerx) and player.direction == 'right':
                    self.kill()
                    player.score += 1
            if player.type_action != 'Attack':
                player.type_action = 'TakingDame'
                player.frame = 0
                player.heart -= 1
                if player.hero_rect_refer_game.centerx > (self.rect.centerx):
                    # Change direction if player after monster
                    player.direction = 'left'
                    player.Back_TakingDame = 10
                else:
                    # Change direction if player before monster
                    player.direction = 'right'
                    player.Back_TakingDame = -10      