import pygame
from settings import *
from supports import *
from sprites  import Generic
from timer    import Timer

from pygame.math import Vector2
from random      import randint,choice

class Sky:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.full_image = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.start_color = [255,255,255]
		self.end_color = [38,101,189]
		self.speed = 2

	def display(self,dt):
		for index,value in enumerate(self.end_color):
			if self.start_color[index] > value:
				self.start_color[index] -= self.speed * dt
		self.full_image.fill(self.start_color)
		self.screen.blit(self.full_image,(0,0),special_flags=pygame.BLEND_RGBA_MULT)

class Rain:
	def __init__(self,all_sprites):
		self.all_sprites = all_sprites
		self.rain_floor = import_folder("../graphics/rain/floor")
		self.rain_drops = import_folder("../graphics/rain/drops")
		self.floor_w,self.floor_h = pygame.image.load("../graphics/world/ground.png").get_size()

	def create_floor(self):
		image = choice(self.rain_floor)
		pos = (randint(0,self.floor_w),randint(0,self.floor_h))
		Drop(self.all_sprites,pos,image,False,LAYERS["rain floor"])

	def create_drops(self):
		image = choice(self.rain_drops)
		pos = (randint(0,self.floor_w),randint(0,self.floor_h))
		Drop(self.all_sprites,pos,image,True,LAYERS["rain drops"])

	def update(self):
		self.create_floor()
		self.create_drops()

class Drop(Generic):
	def __init__(self,groups,pos,image,moving,z):
		super().__init__(groups,pos,image,z)
		self.lifetime = Timer(randint(400,600))
		self.lifetime.activate()
		# Moving
		self.moving = moving
		if self.moving:
			self.pos = Vector2(self.rect.topleft)
			self.direction = Vector2(-2,4)
			self.speed = randint(200,250)

	def move(self,dt):
		if self.moving:
			self.pos += self.direction * self.speed * dt
			self.rect.topleft = round(self.pos.x),(round(self.pos.y))

	def update(self,dt):
		self.move(dt)
		self.lifetime.update()
		if not self.lifetime.active: self.kill()