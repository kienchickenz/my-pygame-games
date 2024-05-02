import pygame,sys
from settings import *
from random   import randint,uniform
from pygame.math import Vector2

class Ship(pygame.sprite.Sprite):
	def __init__(self,group):
		super().__init__(group)
		self.image = pygame.image.load("../graphics/ship.png").convert_alpha() 
		self.rect  = self.image.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
		self.mask  = pygame.mask.from_surface(self.image)
		self.shoot_time = 0
		self.can_shoot  = True
		self.laser_sound = pygame.mixer.Sound("../musics/laser.ogg")
		self.laser_sound.set_volume(0.5)

	def update(self):
		self.move()
		self.shoot()
		self.cooldown()
		self.detect_collision()

	def move(self):
		pos = pygame.mouse.get_pos()
		self.rect.center = pos

	def shoot(self):
		if pygame.mouse.get_pressed()[0] and self.can_shoot:
			Laser(self.rect.midtop,laser_group)
			self.laser_sound.play()
			self.can_shoot  = False
			self.shoot_time = pygame.time.get_ticks()

	def cooldown(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time-self.shoot_time>SHOOT_COOLDOWN:
				self.can_shoot = True
				
	def detect_collision(self):
		if pygame.sprite.spritecollide(self,meteor_group,False):
			if pygame.sprite.spritecollide(self,meteor_group,False,pygame.sprite.collide_mask):
				sys.exit()

class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load("../graphics/laser.png").convert_alpha()
		self.rect  = self.image.get_rect(midbottom=pos)
		self.mask  = pygame.mask.from_surface(self.image)
		self.pos   = Vector2(self.rect.topleft)
		self.direction = Vector2(0,-1)
		self.speed = BULLET_SPEED
		self.explosion_sound = pygame.mixer.Sound("../musics/explosion.ogg")

	def update(self):
		self.pos += self.direction*self.speed*dt
		self.rect.topleft = (self.pos.x,round(self.pos.y))
		self.detect_collision()
		if self.rect.bottom < 0: self.kill()

	def detect_collision(self):
		if pygame.sprite.spritecollide(self,meteor_group,False):
			if pygame.sprite.spritecollide(self,meteor_group,True,pygame.sprite.collide_mask):
				self.kill()
				self.explosion_sound.play()

class Meteor(pygame.sprite.Sprite):
	def __init__(self,group):
		super().__init__(group)
		pos_x = randint(-100,WINDOW_WIDTH+100)
		pos_y = randint(-150,-50)
		self.scaled_image = pygame.image.load("../graphics/meteor.png").convert_alpha()
		self.image = pygame.transform.rotozoom(
			surface=self.scaled_image,
			angle=0,
			scale=uniform(0.5,1.5)
		)
		self.rect = self.image.get_rect(midbottom=(pos_x,pos_y))
		self.mask = pygame.mask.from_surface(self.image)
		self.pos       = Vector2(self.rect.topleft)
		self.direction = Vector2(uniform(-0.5,0.5),1)
		self.speed     = randint(400,700)
		self.rotation = 0
		self.rotation_speed = randint(20,40)

	def update(self):
		self.pos += self.direction*self.speed*dt
		self.rect.topleft = (self.pos.x,round(self.pos.y))
		self.rotate()
		if self.rect.top > WINDOW_HEIGHT: self.kill()

	def rotate(self):
		self.rotation += self.rotation_speed*dt
		self.image     = pygame.transform.rotozoom(
			surface=self.scaled_image,
			angle=self.rotation,
			scale=1
		)
		self.rect = self.image.get_rect(center=self.rect.center)
		self.mask = pygame.mask.from_surface(self.image)

class Score:
	def __init__(self):
		self.font = pygame.font.Font("../fonts/subatomic.ttf",SCORE_SIZE)
		
	def draw(self):
		score_text = pygame.time.get_ticks()//1000
		score = self.font.render(f"Score: {score_text}",True,SCORE_COLOR)
		score_rect = score.get_rect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT-SCORE_OFFSET))
		screen.blit(score,score_rect)
		pygame.draw.rect(
			screen,
			SCORE_COLOR,
			score_rect.inflate(100,30),
			width=8,
			border_radius=5
		)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My fifth python game")
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock  = pygame.time.Clock()
background = pygame.image.load("../graphics/background.png").convert()
spaceship_group = pygame.sprite.Group()
laser_group     = pygame.sprite.Group()
meteor_group    = pygame.sprite.Group() 
ship  = Ship(spaceship_group)
score = Score() 
meteor_timer = pygame.USEREVENT+1
pygame.time.set_timer(meteor_timer,METEOR_SPAWNING_SPEED)
bg_music = pygame.mixer.Sound("../musics/music.ogg")
bg_music.set_volume(0.5)
bg_music.play(loops=-1)
while True:
	dt = clock.tick()/1000
	for event in pygame.event.get():
		if event.type==pygame.QUIT:                              sys.exit()
		if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
		if event.type==meteor_timer: Meteor(meteor_group)
	screen.blit(background,(0,0))
	score.draw()
	spaceship_group.update()
	laser_group.update()
	meteor_group.update()
	spaceship_group.draw(screen)
	laser_group.draw(screen)
	meteor_group.draw(screen)
	pygame.display.update()