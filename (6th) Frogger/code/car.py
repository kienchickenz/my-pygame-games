<<<<<<< HEAD
import pygame
from os     import walk
from random import choice
from settings    import *
from pygame.math import Vector2
class Car(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.name = "car"
		for _,_,files in walk("../graphics/cars"): car_name = choice(files)
		self.image  = pygame.image.load(f"../graphics/cars/{car_name}").convert_alpha()
		self.rect   = self.image.get_rect(center=pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height/2)
		self.pos    = Vector2(self.rect.center)
		if self.pos.x < 500:
			self.direction = Vector2(1,0)
		else:
			self.direction = Vector2(-1,0)
			self.image = pygame.transform.flip(self.image,flip_x=True,flip_y=False)
		self.speed = CAR_SPEED
	
	def update(self,dt):
		self.pos += self.direction*self.speed*dt
		self.hitbox.center = (round(self.pos.x),round(self.pos.y))
		self.rect.center   = (round(self.pos.x),round(self.pos.y))
=======
import pygame
from os     import walk
from random import choice
from settings    import *
from pygame.math import Vector2
class Car(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.name = "car"
		for _,_,files in walk("../graphics/cars"): car_name = choice(files)
		self.image  = pygame.image.load(f"../graphics/cars/{car_name}").convert_alpha()
		self.rect   = self.image.get_rect(center=pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height/2)
		self.pos    = Vector2(self.rect.center)
		if self.pos.x < 500:
			self.direction = Vector2(1,0)
		else:
			self.direction = Vector2(-1,0)
			self.image = pygame.transform.flip(self.image,flip_x=True,flip_y=False)
		self.speed = CAR_SPEED
	
	def update(self,dt):
		self.pos += self.direction*self.speed*dt
		self.hitbox.center = (round(self.pos.x),round(self.pos.y))
		self.rect.center   = (round(self.pos.x),round(self.pos.y))
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
		if not -200 < self.rect.x < 3400: self.kill()