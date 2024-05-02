import pygame
from pygame.math import Vector2
from random      import randint

from settings import *

class Generic(pygame.sprite.Sprite):
	def __init__(self,groups,pos,image,z=LEVEL_LAYERS["main"]):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(topleft=pos)
		self.z = z

class Block(Generic):
	def __init__(self,groups,pos,size):
		surf = pygame.Surface(size)
		super().__init__(groups,pos,surf)

class Cloud(Generic):
	def __init__(self,groups,pos,image,left_limit):
		super().__init__(groups,pos,image,LEVEL_LAYERS["clouds"])
		self.left_limit = left_limit
		# Movement
		self.pos = Vector2(self.rect.topleft)
		self.speed = randint(20,50)

	def move(self,dt):
		self.pos.x -= self.speed * dt
		self.rect.x = round(self.pos.x)

	def update(self,dt):
		self.move(dt)
		if self.rect.x <= self.left_limit: self.kill()

# Animated objects
class Animated(Generic):
	def __init__(self,groups,pos,images,z=LEVEL_LAYERS["main"]):
		self.animation = images
		self.image_index = 0
		super().__init__(groups,pos,self.animation[self.image_index],z)

	def animate(self,dt):
		self.image_index += ANIMATION_SPEED*dt
		if self.image_index >= len(self.animation): self.image_index = 0
		self.image = self.animation[int(self.image_index)]

	def update(self,dt):
		self.animate(dt)

class Particle(Animated):
	def __init__(self,groups,pos,images):
		super().__init__(groups,pos,images)
		self.rect = self.image.get_rect(center=pos)

	def animate(self,dt):
		self.image_index += ANIMATION_SPEED*dt
		if self.image_index >= len(self.animation): 
			self.kill()
		else:
			self.image = self.animation[int(self.image_index)]

class Coin(Animated):
	def __init__(self,groups,pos,images,coin_type):
		super().__init__(groups,pos,images)
		self.rect.center = pos
		self.coin_type = coin_type
