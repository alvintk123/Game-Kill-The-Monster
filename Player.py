import pygame

# Player display coordinates relative to background
class Player():
    def __init__(self,x,y,width,height,list_animation_hero,WINDOWWIDTH,WINDOWHEIGHT):
        self.x, self.y, self.width, self.height, self.WINDOWHEIGHT, self.WINDOWWIDTH = x, y, width, height, WINDOWHEIGHT, WINDOWWIDTH
        self.list_animation_hero = list_animation_hero
        # type of initial action 
        self.type_action = 'Stand'
        # control animation
        self.frame = 0
        #
        self.hero = self.list_animation_hero[self.type_action][self.frame]
        self.hero = pygame.transform.scale(self.hero,(self.width,self.height))
        # The rect displaying coordinates relative to the background's coordinate axis
        # This background's coordinate axis of player is used to change position

        self.hero_rect = self.hero.get_rect(topleft = (self.x,self.y)) # root
        # create an other rect displaying coordinates relative to the game's coordinate axis instead of Background's 
        # This game's coordinate axis of player is only used to compare
        self.hero_rect_refer_game = self.hero.get_rect(topleft = (self.x,self.y)) # root
        
        # direction
        self.direction = 'right'
        #
        self.movement = 0
        self.flag_jump = False
        # Bottom of player
        self.BOTTOM = self.WINDOWHEIGHT
        self.speed = 5
        # Time initial
        self.Time_init = pygame.time.get_ticks()
        # Back Distance due to taking dame
        self.Back_TakingDame = 0
        # Score
        self.score = 0
        self.heart = 5
        # check if has win
        self.Win = False
    def draw(self,DISPLAYSURF,color): 
        self.update_animation()
        # self.Rect = pygame.draw.rect(DISPLAYSURF,(255,255,0),(self.hero_rect_refer_game.left,self.hero_rect_refer_game.top,self.width*0.5,self.height*0.5),2)
        # DISPLAYSURF.blit(self.hero,(self.hero_rect_refer_game.left-12 ,self.hero_rect_refer_game.top-15))
        #self.Rect = pygame.draw.rect(DISPLAYSURF,(255,255,0),(self.hero_rect_refer_game.left,self.hero_rect_refer_game.top,self.width,self.height),2)
        DISPLAYSURF.blit(self.hero,(self.hero_rect_refer_game.left ,self.hero_rect_refer_game.top))

        # draw score
        font1 = pygame.font.Font('freesansbold.ttf',30)
        self.text1 = font1.render('Score {}'.format(self.score),True,color)
        DISPLAYSURF.blit(self.text1,(self.WINDOWWIDTH-140,20))

    # Note: Always set frame to 0 when changing type 
    def update_animation(self):
        Cooldown = 50
        time_now = pygame.time.get_ticks()
        # print('self.frame',self.frame)
        # print('self.type',self.type_action)
        self.hero = self.list_animation_hero[self.type_action][self.frame]
        self.hero = pygame.transform.scale(self.hero,(self.width,self.height))
        # flip the image if direction is left
        if self.direction == 'left':
            self.hero = pygame.transform.flip(self.hero,True,False)  

        if time_now - self.Time_init > Cooldown:
            self.Time_init = time_now
            self.frame += 1
            if self.frame >= len(self.list_animation_hero[self.type_action]):
                # Change to 'Stand' type when finish 'Attack' or 'TakingDame'
                if self.type_action == 'Attack' or self.type_action == 'TakingDame':
                    self.type_action = 'Stand'
                    self.frame = 0
                # Maintain the last animation when jumping or falling
                if self.type_action == 'Jump' or self.type_action == 'Fall':
                    self.frame = len(self.list_animation_hero[self.type_action])-1
                # reset animation if not jumping
                else:
                    self.frame = 0
    

    def Heart(self,DISPLAYSURF,life):
        for i in range(self.heart):
            life = pygame.transform.scale(life,(30,30))
            DISPLAYSURF.blit(life,(i*50,10))
        if self.heart <= 0:
            return True
        else:
            return False

    def move(self,bg,left,right,wood_group):
        # Take the initial position
        pos_1x = self.hero_rect.centerx
        pos_1y = self.hero_rect.centery 

        # Keep from moving when you in 'takingDame' type
        if not abs(self.Back_TakingDame) >= 10/2:
            # Move right
            if right:
                # change the direction
                if self.direction != 'right':
                    self.direction = 'right'
                self.hero_rect.centerx += self.speed
                # change type of action
                if self.type_action != 'Move' and self.type_action !=  'Jump' and self.type_action !=  'Fall' and self.type_action !=  'Attack':   #Avoid self.frame always 0 when move and change type when jumping and falling
                    self.type_action = 'Move'
                    self.frame = 0
            # Move left
            if left:
                # change the direction 
                if self.direction != 'left':
                    self.direction = 'left'
                self.hero_rect.centerx -= self.speed
                # change type of action
                if self.type_action != 'Move' and self.type_action !=  'Jump' and self.type_action !=  'Fall' and self.type_action !=  'Attack':    #Avoid self.frame always 0 when move and change type when jumping and falling
                    self.type_action = 'Move'
                    self.frame = 0
        # Right boundary of game
        if self.hero_rect.right > bg.BG.get_width():
            self.hero_rect.right = bg.BG.get_width()             
        # Left boundary of game
        if self.hero_rect.left < 0:
            self.hero_rect.left = 0 

        # Apply Gravity 
        self.hero_rect.bottom += self.movement
        
        if self.hero_rect.bottom >= self.BOTTOM:
            self.movement = 0
            self.hero_rect.bottom = self.BOTTOM
            self.flag_jump = True

        # Go Back due to Taking Dame
        self.hero_rect.centerx += self.Back_TakingDame
        if self.Back_TakingDame > 0:
            self.Back_TakingDame -= 1
        if self.Back_TakingDame < 0 :
            self.Back_TakingDame += 1

        # Take the following position
        pos_2x = self.hero_rect.centerx
        pos_2y = self.hero_rect.centery 

        # Check if stand
        if pos_1x == pos_2x and pos_1y == pos_2y and self.type_action != 'Attack' and self.type_action != 'TakingDame':
            if self.type_action != 'Stand':
                self.type_action = 'Stand'
                self.frame = 0
        if pos_2y > pos_1y:
            if self.type_action != 'Fall' and self.type_action != 'Attack' and self.type_action != 'TakingDame':
                self.type_action = 'Fall'
                self.frame = 0 

        #Convert from background's reference coordinate to game's reference coordinate 
        self.hero_rect_refer_game.centerx = self.hero_rect.centerx + bg.x
        self.hero_rect_refer_game.centery = self.hero_rect.centery + bg.y     
    def Check_on_object(self,object_group):
        pos = []
        for object in object_group:
            if self.hero_rect_refer_game.centery <= object.rect.centery:
                pos.append(object.rect.top)
        # Check on the taller object
        if len(pos):
            return min(pos) 
        else:
            return False
    def Check_under_object(self,object_group):
        pos = []
        for object in object_group:
            if self.hero_rect_refer_game.centery >= object.rect.centery:
                pos.append(object.rect.bottom)
        if len(pos):
            return max(pos)
        else:
            return False
        return False
    def Check_inside_object(self,object_group):
        for object in object_group:
            if self.hero_rect_refer_game.centerx >= object.rect.left and self.hero_rect_refer_game.centerx <= object.rect.right:
                self.object_active.append(object)
        if len(self.object_active):
            return True
        else:
            return False
    def Collide_Branch(self,wood_group):
        self.object_active = []
        if self.Check_inside_object(wood_group):
            check_top = self.Check_under_object(self.object_active)
            check_bot = self.Check_on_object(self.object_active)
            if check_top:
                if self.hero_rect_refer_game.top <= check_top:
                    self.movement = 0
                    self.hero_rect.top = check_top
            # On object
            if check_bot and self.hero_rect_refer_game.bottom >= check_bot :
                self.BOTTOM = check_bot
            else:
                self.BOTTOM = self.WINDOWHEIGHT
        else:
            self.BOTTOM = self.WINDOWHEIGHT
