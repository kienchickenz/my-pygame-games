import pygame
from settings import *
from pygame.math import Vector2
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,image,groups,z):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(topleft=pos)
		self.z = z

class CollisionTile(Tile):
	def __init__(self,pos,image,groups):
		super().__init__(pos,image,groups,LAYERS["Main"])
		self.old_rect = self.rect.copy()

class MovingPlatform(CollisionTile):
	def __init__(self,pos,image,groups):
		super().__init__(pos,image,groups)
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(0,-1)
		self.speed = PLATFORM_SPEED

	def move(self,dt):
		self.pos.y += self.direction.y*self.speed*dt
		self.rect.topleft = (round(self.pos.x),round(self.pos.y))

	def update(self,dt):
		self.old_rect = self.rect.copy()
		self.move(dt)