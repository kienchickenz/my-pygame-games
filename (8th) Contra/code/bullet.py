<<<<<<< HEAD
import pygame
from settings import *
from pygame.math import Vector2
class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,image,direction,groups):
		super().__init__(groups)
		self.image = image
		if direction.x < 0:
			self.image = pygame.transform.flip(image,flip_x=True,flip_y=False)
		self.rect  = self.image.get_rect(center=pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.z = LAYERS["Main"]
		# Move
		self.pos = Vector2(self.rect.center)
		self.direction = direction
		self.speed = BULLET_SPEED
		self.start_time = pygame.time.get_ticks()

	def move(self,dt):
		self.pos += self.direction*self.speed*dt
		self.rect.center = (round(self.pos.x),round(self.pos.y))

	def update(self,dt):
		self.move(dt)
		if pygame.time.get_ticks() - self.start_time > BULLET_DURATION:
			self.kill()

class FireAnimation(pygame.sprite.Sprite):
	def __init__(self,entity,image_list,direction,groups):
		super().__init__(groups)
		# Setup
		self.entity = entity
		self.image_list = image_list
		if direction.x < 0:
			self.image_list = [pygame.transform.flip(image,True,False) for image in image_list]
		# Image
		self.image_index = 0
		self.image = self.image_list[self.image_index]
		# Offset
		x_offset = 60 if direction.x > 0 else -60
		y_offset = -20 if not self.entity.duck else 10
		self.offset = Vector2(x_offset,y_offset)
		# Position
		self.rect  = self.image.get_rect(center=self.entity.rect.center+self.offset)
		self.z = LAYERS["Main"]

	def animate(self,dt):
		self.image_index += FIRE_ANIMATION_SPEED*dt
		if self.image_index >= len(self.image_list): 
			self.kill()
		else:
			self.image = self.image_list[int(self.image_index)]

	def move(self):
		self.rect.center = self.entity.rect.center + self.offset

	def update(self,dt):
		self.animate(dt)
=======
import pygame
from settings import *
from pygame.math import Vector2
class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,image,direction,groups):
		super().__init__(groups)
		self.image = image
		if direction.x < 0:
			self.image = pygame.transform.flip(image,flip_x=True,flip_y=False)
		self.rect  = self.image.get_rect(center=pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.z = LAYERS["Main"]
		# Move
		self.pos = Vector2(self.rect.center)
		self.direction = direction
		self.speed = BULLET_SPEED
		self.start_time = pygame.time.get_ticks()

	def move(self,dt):
		self.pos += self.direction*self.speed*dt
		self.rect.center = (round(self.pos.x),round(self.pos.y))

	def update(self,dt):
		self.move(dt)
		if pygame.time.get_ticks() - self.start_time > BULLET_DURATION:
			self.kill()

class FireAnimation(pygame.sprite.Sprite):
	def __init__(self,entity,image_list,direction,groups):
		super().__init__(groups)
		# Setup
		self.entity = entity
		self.image_list = image_list
		if direction.x < 0:
			self.image_list = [pygame.transform.flip(image,True,False) for image in image_list]
		# Image
		self.image_index = 0
		self.image = self.image_list[self.image_index]
		# Offset
		x_offset = 60 if direction.x > 0 else -60
		y_offset = -20 if not self.entity.duck else 10
		self.offset = Vector2(x_offset,y_offset)
		# Position
		self.rect  = self.image.get_rect(center=self.entity.rect.center+self.offset)
		self.z = LAYERS["Main"]

	def animate(self,dt):
		self.image_index += FIRE_ANIMATION_SPEED*dt
		if self.image_index >= len(self.image_list): 
			self.kill()
		else:
			self.image = self.image_list[int(self.image_index)]

	def move(self):
		self.rect.center = self.entity.rect.center + self.offset

	def update(self,dt):
		self.animate(dt)
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
		self.move()