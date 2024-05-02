<<<<<<< HEAD
import pygame,sys
from settings import *
from player   import Player
from car      import Car
from pygame.math import Vector2
from random   import choice,randint
from sprite   import SimpleSprite,LongSprite
class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = Vector2(0,0)
		self.background = pygame.image.load("../graphics/main/map.png").convert()
		self.foreground = pygame.image.load("../graphics/main/overlay.png").convert_alpha() 

	def customize_draw(self):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		screen.blit(self.background,-self.offset)
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			screen.blit(sprite.image,offset_pos)
		screen.blit(self.foreground,-self.offset)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My sixth python game")
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock  = pygame.time.Clock()
all_sprites  = AllSprites()
obstacle_sprites = pygame.sprite.Group()
player = Player((2062,3274),all_sprites,obstacle_sprites)
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer,CAR_SPAWNING_SPEED)
car_pos_list = []
for file_name,pos_list in SIMPLE_OBJECTS.items():
	path  = f"../graphics/objects/simple/{file_name}.png"
	image = pygame.image.load(path).convert_alpha()
	for pos in pos_list:
		SimpleSprite(image,pos,[all_sprites,obstacle_sprites])
for file_name,pos_list in LONG_OBJECTS.items():
	path  = f"../graphics/objects/long/{file_name}.png"
	image = pygame.image.load(path).convert_alpha()
	for pos in pos_list:
		LongSprite(image,pos,[all_sprites,obstacle_sprites])
font = pygame.font.Font(None,FONT_SIZE)
text = font.render("You Won!",True,FONT_COLOR)
text_rect = text.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
bg_music = pygame.mixer.Sound("../musics/music.ogg")
bg_music.play(loops=-1)
while True:
	dt = clock.tick()/1000
	for event in pygame.event.get():
		if event.type==pygame.QUIT                             : sys.exit()
		if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
		if event.type==car_timer:
			random_pos = choice(CAR_START_POSITIONS)
			if random_pos not in car_pos_list:
				car_pos_list.append(random_pos)
				car_pos = (random_pos[0],random_pos[1]+randint(-10,10))
				Car(car_pos,[all_sprites,obstacle_sprites])
			if len(car_pos_list) > 5: del car_pos_list[0]
	screen.fill("grey12")
	if player.pos.y>=1180:
		all_sprites.update(dt)
		all_sprites.customize_draw()
	else:
		screen.fill(ENDING_BG_COLOR)
		screen.blit(text,text_rect)
=======
import pygame,sys
from settings import *
from player   import Player
from car      import Car
from pygame.math import Vector2
from random   import choice,randint
from sprite   import SimpleSprite,LongSprite
class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = Vector2(0,0)
		self.background = pygame.image.load("../graphics/main/map.png").convert()
		self.foreground = pygame.image.load("../graphics/main/overlay.png").convert_alpha() 

	def customize_draw(self):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		screen.blit(self.background,-self.offset)
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			screen.blit(sprite.image,offset_pos)
		screen.blit(self.foreground,-self.offset)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My sixth python game")
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock  = pygame.time.Clock()
all_sprites  = AllSprites()
obstacle_sprites = pygame.sprite.Group()
player = Player((2062,3274),all_sprites,obstacle_sprites)
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer,CAR_SPAWNING_SPEED)
car_pos_list = []
for file_name,pos_list in SIMPLE_OBJECTS.items():
	path  = f"../graphics/objects/simple/{file_name}.png"
	image = pygame.image.load(path).convert_alpha()
	for pos in pos_list:
		SimpleSprite(image,pos,[all_sprites,obstacle_sprites])
for file_name,pos_list in LONG_OBJECTS.items():
	path  = f"../graphics/objects/long/{file_name}.png"
	image = pygame.image.load(path).convert_alpha()
	for pos in pos_list:
		LongSprite(image,pos,[all_sprites,obstacle_sprites])
font = pygame.font.Font(None,FONT_SIZE)
text = font.render("You Won!",True,FONT_COLOR)
text_rect = text.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
bg_music = pygame.mixer.Sound("../musics/music.ogg")
bg_music.play(loops=-1)
while True:
	dt = clock.tick()/1000
	for event in pygame.event.get():
		if event.type==pygame.QUIT                             : sys.exit()
		if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
		if event.type==car_timer:
			random_pos = choice(CAR_START_POSITIONS)
			if random_pos not in car_pos_list:
				car_pos_list.append(random_pos)
				car_pos = (random_pos[0],random_pos[1]+randint(-10,10))
				Car(car_pos,[all_sprites,obstacle_sprites])
			if len(car_pos_list) > 5: del car_pos_list[0]
	screen.fill("grey12")
	if player.pos.y>=1180:
		all_sprites.update(dt)
		all_sprites.customize_draw()
	else:
		screen.fill(ENDING_BG_COLOR)
		screen.blit(text,text_rect)
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
	pygame.display.update()