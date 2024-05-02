<<<<<<< HEAD
import pygame,sys,time
from settings import *
from random   import randint,choice

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
    
    def animate_player(self,dt):
        if self.rect.bottom < 300: self.image = self.player_jump
        else: 
            self.player_index += PLAYER_ANIMATION_SPEED * dt
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self,dt):
        self.player_input()
        self.apply_gravity()
        self.animate_player(dt)
    
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
        self.pos   = pygame.math.Vector2(self.rect.topleft)

    def move_enemy(self,dt): 
        self.pos.x -= ENEMY_SPEED * dt
        self.rect.x = round(self.pos.x)

    def animate_enemy(self,dt):
        self.animation_index += ENEMY_ANIMATION_SPEED * dt
        if self.animation_index >= len(self.images): self.animation_index = 0
        self.image = self.images[int(self.animation_index)]

    def clear(self):
        if self.rect.x <= -50:
            self.kill()

    def update(self,dt):
        self.clear()
        self.move_enemy(dt)
        self.animate_enemy(dt)

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

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My first python game")
window = pygame.display.set_mode([WIDTH,HEIGHT])
clock  = pygame.time.Clock()
prev_time = time.time()
font = pygame.font.Font("fonts/ThaleahFat.ttf",FONT_SIZE)
game_over = True
the_player = pygame.sprite.GroupSingle()
the_player.add(Player())
the_enemies = pygame.sprite.Group()
# convert(): png-files -> sth pygame can work easily
# convert_alpha():same as convert() but remove the non-color parts
sky    = pygame.image.load("graphics/sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,SPAWNING_SPEED)
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
    dt        = time.time() - prev_time
    prev_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()
        if not game_over:
            if event.type == obstacle_timer:
                the_enemies.add(Enemy(choice(["fly","snail","snail","snail"])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    the_player.sprite.rect.bottom = GROUND_LEVEL
                    start_time = pygame.time.get_ticks()//1000
    if not game_over:
        game_over = sprite_collision()
        window.blit(sky,(0,SKY_LEVEL))      
        window.blit(ground,(0,GROUND_LEVEL))
        the_player.draw(window)
        the_player.update(dt)
        the_enemies.draw(window)
        the_enemies.update(dt)
        score = display_score()
    else:
        final_score = font.render(f"Your score: {score}",False,ENDGAME_TEXT_COLOR)
        final_score_rect = final_score.get_rect(midbottom=(WIDTH/2,FINAL_SCORE_Y))
        window.fill(ENDGAME_BACKGROUND_COLOR)
        window.blit(name,name_rect)
        window.blit(player_stand,player_stand_rect)
        window.blit(instruction,instruction_rect)
        if score != 0: window.blit(final_score,final_score_rect)
    pygame.display.update()
=======
import pygame,sys,time
from settings import *
from random   import randint,choice

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
    
    def animate_player(self,dt):
        if self.rect.bottom < 300: self.image = self.player_jump
        else: 
            self.player_index += PLAYER_ANIMATION_SPEED * dt
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self,dt):
        self.player_input()
        self.apply_gravity()
        self.animate_player(dt)
    
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
        self.pos   = pygame.math.Vector2(self.rect.topleft)

    def move_enemy(self,dt): 
        self.pos.x -= ENEMY_SPEED * dt
        self.rect.x = round(self.pos.x)

    def animate_enemy(self,dt):
        self.animation_index += ENEMY_ANIMATION_SPEED * dt
        if self.animation_index >= len(self.images): self.animation_index = 0
        self.image = self.images[int(self.animation_index)]

    def clear(self):
        if self.rect.x <= -50:
            self.kill()

    def update(self,dt):
        self.clear()
        self.move_enemy(dt)
        self.animate_enemy(dt)

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

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My first python game")
window = pygame.display.set_mode([WIDTH,HEIGHT])
clock  = pygame.time.Clock()
prev_time = time.time()
font = pygame.font.Font("fonts/ThaleahFat.ttf",FONT_SIZE)
game_over = True
the_player = pygame.sprite.GroupSingle()
the_player.add(Player())
the_enemies = pygame.sprite.Group()
# convert(): png-files -> sth pygame can work easily
# convert_alpha():same as convert() but remove the non-color parts
sky    = pygame.image.load("graphics/sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,SPAWNING_SPEED)
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
    dt        = time.time() - prev_time
    prev_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()
        if not game_over:
            if event.type == obstacle_timer:
                the_enemies.add(Enemy(choice(["fly","snail","snail","snail"])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    the_player.sprite.rect.bottom = GROUND_LEVEL
                    start_time = pygame.time.get_ticks()//1000
    if not game_over:
        game_over = sprite_collision()
        window.blit(sky,(0,SKY_LEVEL))      
        window.blit(ground,(0,GROUND_LEVEL))
        the_player.draw(window)
        the_player.update(dt)
        the_enemies.draw(window)
        the_enemies.update(dt)
        score = display_score()
    else:
        final_score = font.render(f"Your score: {score}",False,ENDGAME_TEXT_COLOR)
        final_score_rect = final_score.get_rect(midbottom=(WIDTH/2,FINAL_SCORE_Y))
        window.fill(ENDGAME_BACKGROUND_COLOR)
        window.blit(name,name_rect)
        window.blit(player_stand,player_stand_rect)
        window.blit(instruction,instruction_rect)
        if score != 0: window.blit(final_score,final_score_rect)
    pygame.display.update()
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
    clock.tick(FPS)