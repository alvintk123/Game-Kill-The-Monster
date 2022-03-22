import pygame, sys
from pygame.locals import *
from Background import Background
from Player import Player
from Monster import monster
from Object import object
from Destination import Destination

pygame.init()
# fps
fpsclock = pygame.time.Clock()
FPS = 30

# Variable
WINDOWWIDTH = 500
WINDOWHEIGHT = 700
Hero_Width = 50
Hero_Height = 50
game_over = False

# color
GRAY = (100,100,100)
BLUE = (0, 0,255)
YELLOW = (255 , 255 , 0)
CYAN = (0, 255 ,255)
# screen
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
# dir
dir_ = 'Figure/Player/'
dir1_ = 'Figure/Monster/'
dir2_ = 'Figure/assert/'
# load image
BG = pygame.image.load(dir2_ + 'backGround.png').convert_alpha()
wood = pygame.image.load(dir2_ +'woods.png').convert_alpha()
Des_ = pygame.image.load(dir2_ +'House.png').convert_alpha()
HEART = pygame.image.load(dir2_ +'Heart.png').convert_alpha()

type_ = {
    "Attack": [],
    "Defend": [],
    "Stand": [],
    "Move": [],
    "Dead": [],
    "Fall": [],
    "Jump": [],
    "TakingDame" : []
}
type1_ = {
    "Move": [],
    "Dead": [],
}
#print(Destination)
# Tree follow BackGround
# BackGround move left 
def draw_text(text,Font,color,posx,posy):
    Text_sur = Font.render(text,True,color)
    Text_rect = Text_sur.get_rect(center = (posx,posy))
    DISPLAYSURF.blit(Text_sur,Text_rect)
def Win(bg,Player):
	if bg.cover_speed < WINDOWWIDTH:
		bg.cover_speed += 20
		pygame.draw.rect(DISPLAYSURF,CYAN,(0,0,bg.cover_speed,WINDOWHEIGHT))
	Font = pygame.font.Font('freesansbold.ttf',50)
	Font1 = pygame.font.Font('freesansbold.ttf',40)
	draw_text('YOU WIN',Font,YELLOW,WINDOWWIDTH/2,WINDOWHEIGHT/2)
	draw_text('You get {} scores'.format(Player.score),Font1,YELLOW,WINDOWWIDTH/2,WINDOWHEIGHT/2+50)
def Game_over(bg,Player):
    if bg.cover_speed < WINDOWWIDTH:
        bg.cover_speed += 20
        pygame.draw.rect(DISPLAYSURF,YELLOW,(0,0,bg.cover_speed,WINDOWHEIGHT))
    Font = pygame.font.Font('freesansbold.ttf',50)
    Font1 = pygame.font.Font('freesansbold.ttf',40)
    draw_text('Game Over',Font,CYAN,WINDOWWIDTH/2,WINDOWHEIGHT/2)
    draw_text('You get {} scores'.format(Player.score),Font1,CYAN,WINDOWWIDTH/2,WINDOWHEIGHT/2+50)

def reset_game():
    # Remove all sprite in Group
    wood_group.empty()
    monster_group.empty()
    for i in Number_Wood:
        woods = object(wood,*i)
        wood_group.add(woods)
    for i in Number_Monster:
        monters = monster(type1_,*i)
        monster_group.add(monters)
    player = Player(0,int(WINDOWHEIGHT-Hero_Height),Hero_Width,Hero_Height,type_,WINDOWWIDTH,WINDOWHEIGHT)
    bg = Background(BG,0,0,WINDOWWIDTH,WINDOWHEIGHT)
    Des = Destination(Des_,1000-100,200,100,100)
    return wood_group, monster_group, player, bg, Des

# Load image of hero
list_animation_hero =  []
for type_action in type_.keys():
    #print(type_action)
    n = 0 
    try:
        while True:
            n += 1
            action = pygame.image.load(dir_ + type_action + '/{}.png'.format(n)).convert_alpha()
            #action = pygame.transform.scale(action,(Hero_Width*5,Hero_Height*5))
            type_[type_action].append(action)
    except FileNotFoundError:
        continue
# Load image of monster
list_animation_monster = []
for type_action in type1_.keys():
    n = 0
    try:
        while True:
            n += 1
            action = pygame.image.load(dir1_ + type_action + f'/{n}.png').convert_alpha()
            type1_[type_action].append(action)
    except FileNotFoundError:
        continue

class Skill(object):
    def __init__(self,img,x,y,width,height,direction,speed):
        object.__init__(self,img,x,y,width,height)
        self.direction = direction
        self.speed = speed
    def update(self,bg):
        pass

Number_Wood = ((200,580,100,30),(200,400,100,30),(350,480,100,30),(600,600,100,30),(750,500,100,30),(850,400,100,30),(950,300,100,30))
Number_Monster = ((400,680,60,40,'right',1,320,470),(350,450,60,40,'left',2,300,400)) #(x,y,width,height,direction,speed,bound_left,bound_right):
wood_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
monster_group_temp = monster_group.copy()
left, right = False, False       
gravity = 1
wood_group, monster_group, player, bg, Des = reset_game()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if player.flag_jump:
                if event.key == K_UP:
                    #player.movement = 0
                    player.movement -= 18
                    player.flag_jump = False
                    player.type_action = 'Jump'
                    player.frame = 0
            if event.key == K_LEFT:
                left = True
            if event.key == K_RIGHT:
                right = True
            if event.key == K_SPACE:
                player.type_action = 'Attack'
                player.frame = 0
            if event.key == K_p:
                game_over = True
            if event.key == K_n:
                wood_group, monster_group, player, bg, Des = reset_game()
                game_over = False
        if event.type == KEYUP:
            if event.key == K_LEFT:
                left = False
            if event.key == K_RIGHT:
                right = False
    if game_over == False and player.Win == False:
        player.movement += gravity
        bg.draw(DISPLAYSURF)
        bg.move(player)
        Des.draw(DISPLAYSURF,bg)
        player.draw(DISPLAYSURF,YELLOW)
        wood_group.draw(DISPLAYSURF)
        wood_group.update(bg)
        monster_group.draw(DISPLAYSURF)
        monster_group.update(bg,player,monster_group)
        player.move(bg,left,right,wood_group)
        player.Collide_Branch(wood_group)
        Des.has_player(DISPLAYSURF,player)
        game_over = player.Heart(DISPLAYSURF,HEART)
    elif game_over == True:
        Game_over(bg,player)
    elif player.Win == True:
        Win(bg,player)
    pygame.display.update()
    fpsclock.tick(FPS)
