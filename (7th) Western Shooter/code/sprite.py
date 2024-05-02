import pygame
from settings import *
from pygame.math import Vector2

class Sprite(pygame.sprite.Sprite):
	def __init__(self,pos,image,groups):
		super().__init__(groups)
		self.image  = image
		self.rect   = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height/3)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,direction,image,groups):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(center=pos)
		self.mask  = pygame.mask.from_surface(self.image)
		self.pos = Vector2(self.rect.center)
		self.direction = direction
		self.speed = BULLET_SPEED

	def update(self,dt):
		self.pos += self.direction*self.speed*dt
		self.rect.center = (round(self.pos.x),round(self.pos.y))		