import pygame
from sys    import exit
from random import randint,choice
WIDTH   = 800
HEIGHT  = 400
FPS_CAP = 60 # max_fps = 60
SKY_IMAGE_HEIGHT    = 300
PLAYER_IMAGE_WIDTH  = 64
PLAYER_IMAGE_HEIGHT = 84
SNAIL_IMAGE_HEIGHT  = 36
SNAIL_IMAGE_WIDTH   = 72
FLY_IMAGE_HEIGHT    = 40
FLY_IMAGE_WIDTH     = 84
FONT_SIZE = 40
# Y_Level
# Game screen
SCORE_Y      = 20
SKY_LEVEL    = 0
GROUND_LEVEL = SKY_LEVEL + SKY_IMAGE_HEIGHT
FLY_Y        = GROUND_LEVEL - PLAYER_IMAGE_HEIGHT - 20
SNAIL_Y      = GROUND_LEVEL
# End game
NAME_Y         = 10
INSTRUCTION_Y  = HEIGHT - 10
FINAL_SCORE_Y  = INSTRUCTION_Y - FONT_SIZE
PLAYER_STAND_Y = FINAL_SCORE_Y - FONT_SIZE - 30
# COLOR
TEXT_COLOR               = (64,64,64)
TEXT_BACKGROUND_COLOR    = "#c0e8ec"
ENDGAME_TEXT_COLOR       = (111,196,169)
ENDGAME_BACKGROUND_COLOR = (94,129,162)
# ANIMATION
ANIMATION_RATE        = 10/60 # images / 60 frames (1 second)
SNAIL_ANIMATION_SPEED = 500 # in milliseconds
FLY_ANIMATION_SPEED   = 200 # in milliseconds
# STATS
SPAWNING_SPEED = 1500 # in milliseconds
ENEMY_SPEED  = 5
GRAVITY_JUMP = -20
GRAVITY      = 1
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk  = [player_walk_1,player_walk_2] 
        self.player_index = 0
        self.player_jump  = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect  = self.image.get_rect(midbottom=(80,GROUND_LEVEL))
        self.jump_sound = pygame.mixer.Sound("musics/jump.ogg")
        self.jump_sound.set_volume(0.4)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == GROUND_LEVEL:
            self.gravity = GRAVITY_JUMP 
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += GRAVITY
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL: self.rect.bottom = GROUND_LEVEL
    def animate_player(self):
        if self.rect.bottom < 300: self.image = self.player_jump
        else: 
            self.player_index += ANIMATION_RATE
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate_player()
    def reset_gravity(self): self.gravity = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.images = [fly_1,fly_2]
            y = FLY_Y
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.images = [snail_1,snail_2]
            y = SNAIL_Y
        self.animation_index = 0
        self.image = self.images[self.animation_index]
        self.rect  = self.image.get_rect(midbottom=(randint(900,1100),y))
    def move_enemy(self):
        self.rect.x -= ENEMY_SPEED
    def animate_enemy(self):
        self.animation_index += ANIMATION_RATE
        if self.animation_index >= len(self.images): self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
    def clear(self):
        if self.rect.x <= -50:
            self.kill()
    def update(self):
        self.clear()
        self.move_enemy()
        self.animate_enemy()
def display_score():
    time = pygame.time.get_ticks()//1000 - start_time
    score      = font.render(f"Score: {time}",False,TEXT_COLOR)
    score_rect = score.get_rect(midtop=(WIDTH/2,SCORE_Y))
    window.blit(score,score_rect)
    return time
def sprite_collision():
    if pygame.sprite.spritecollide(the_player.sprite,the_enemies,False):
        the_enemies.empty()
        return True
    return False
# def move_enemies(enemies):
#     if enemies:
#         for enemy in enemies: enemy.x -= ENEMY_SPEED
#         enemies = [enemy for enemy in enemies if enemy.right > 0]
#     return enemies
# def draw_enemies(enemies):
#     if enemies:
#         for enemy in enemies: 
#             if enemy.bottom == GROUND_LEVEL: window.blit(snail,enemy)
#             else: window.blit(fly,enemy)
# def hit_enemy(player,enemies):
#     if enemies:
#         for enemy in enemies: 
#             if player.colliderect(enemy): return True
#     return False
# def animate_player():
#     global player,player_index
#     if player_rect.bottom < 300: player = player_jump
#     else: 
#         player_index += ANIMATION_RATE
#         if player_index >= len(player_walk): player_index = 0
#         player = player_walk[int(player_index)]
pygame.init()
pygame.display.set_caption("My first python game")
window = pygame.display.set_mode([WIDTH,HEIGHT])
fps    = pygame.time.Clock()
font   = pygame.font.Font("fonts/ThaleahFat.ttf",FONT_SIZE)
game_over = True
the_player = pygame.sprite.GroupSingle()
the_player.add(Player())
the_enemies = pygame.sprite.Group()
# convert(): png-files -> sth pygame can work easily
# convert_alpha():same as convert() but remove the non-color parts
sky    = pygame.image.load("graphics/sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()
# player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
# player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
# player_walk   = [player_walk_1,player_walk_2] 
# player_index  = 0
# player_jump   = pygame.image.load("graphics/player/jump.png").convert_alpha()
# player        = player_walk[player_index]
# player_rect   = player.get_rect(midbottom=(100,GROUND_LEVEL))
# snail_1     = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_2     = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
# snail_list  = [snail_1,snail_2]
# snail_index = 0
# snail       = snail_list[snail_index]
# fly_1     = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
# fly_2     = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
# fly_list  = [fly_1,fly_2]
# fly_index = 0
# fly       = fly_list[fly_index]
# enemies = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,SPAWNING_SPEED)
# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer,SNAIL_ANIMATION_SPEED)
# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer,FLY_ANIMATION_SPEED)
# player_gravity = 0
# END GAME
start_time     = 0
score          = 0
player_stand      = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand      = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(midbottom=(WIDTH/2,PLAYER_STAND_Y))
instruction      = font.render("Press 'Space Bar' to start the game",False,ENDGAME_TEXT_COLOR)
instruction_rect = instruction.get_rect(midbottom=(WIDTH/2,HEIGHT-10))
name      = font.render("Pixel Runner",False,ENDGAME_TEXT_COLOR)
name_rect = name.get_rect(midtop=(WIDTH/2,NAME_Y))
bg_music = pygame.mixer.Sound("musics/bg_music.ogg")
bg_music.play(loops=-1)
while True:
    fps.tick(FPS_CAP)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: exit()
        if not game_over:
            # if event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos):
            #     if player_rect.bottom == GROUND_LEVEL:
            #         player_gravity = GRAVITY_JUMP
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
            #     if player_rect.bottom == GROUND_LEVEL: 
            #         player_gravity = GRAVITY_JUMP
            if event.type == obstacle_timer:
                the_enemies.add(Enemy(choice(["fly","snail","snail","snail"])))
                # if randint(0,1): enemies.append(snail.get_rect(midbottom=(randint(900,1100),GROUND_LEVEL)))
                # else: enemies.append(fly.get_rect(midbottom=(randint(900,1100),GROUND_LEVEL - PLAYER_IMAGE_HEIGHT - 20)))
            # if event.type == fly_animation_timer:
            #     fly = fly_list[1] if fly == fly_list[0] else fly_list[0]
            # if event.type == snail_animation_timer:
            #     snail = snail_list[1] if snail == snail_list[0] else snail_list[0]
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    the_player.sprite.rect.bottom = GROUND_LEVEL
                    start_time = pygame.time.get_ticks()//1000
    if not game_over:
        game_over = sprite_collision()
        # player_gravity += GRAVITY
        # player_rect.y += player_gravity
        # if player_rect.bottom > GROUND_LEVEL: player_rect.bottom = GROUND_LEVEL
        # animate_player()     
        # enemies = move_enemies(enemies) 
        window.blit(sky,(0,SKY_LEVEL))      
        window.blit(ground,(0,GROUND_LEVEL))  
        # window.blit(player,player_rect) 
        the_player.draw(window)
        the_player.update()
        the_enemies.draw(window)
        the_enemies.update()
        # draw_enemies(enemies)
        score = display_score()
    else:
        # enemies.clear()
        final_score = font.render(f"Your score: {score}",False,ENDGAME_TEXT_COLOR)
        final_score_rect = final_score.get_rect(midbottom=(WIDTH/2,FINAL_SCORE_Y))
        window.fill(ENDGAME_BACKGROUND_COLOR)
        window.blit(name,name_rect)
        window.blit(player_stand,player_stand_rect)
        window.blit(instruction,instruction_rect)
        if score != 0: window.blit(final_score,final_score_rect)