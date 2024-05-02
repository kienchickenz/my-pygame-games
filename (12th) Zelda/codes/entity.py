import pygame
from pygame.math import Vector2
from os   import walk

class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.animations = {}

	def import_images(self,path):
		for index,folder in enumerate(walk(path)):
			if index == 0:
				self.animations = {key:[] for key in folder[1]}
			else:
				for file_name in folder[2]:
					path = folder[0].replace("\\","/") + "/" + file_name
					image = pygame.image.load(path).convert_alpha()
					key = folder[0].split("\\")[1]
					self.animations[key].append(image)

	def collision(self,direction):
		for sprite in self.obstacle_sprites.sprites():
			if sprite.hitbox.colliderect(self.hitbox):
				if direction == "horizontal":
					if self.direction.x > 0: # Right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # Left
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.rect.x
				if direction == "vertical":
					if self.direction.y < 0: # Up
						self.hitbox.top = sprite.hitbox.bottom
					if self.direction.y > 0: # Down
						self.hitbox.bottom = sprite.hitbox.top
					self.rect.centery = self.hitbox.centery
					self.pos.y = self.rect.y

	def move(self,dt,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		# Horizontal movement
		self.pos.x += self.direction.x*speed*dt
		self.rect.x = round(self.pos.x)
		self.hitbox.centerx = self.rect.centerx
		self.collision("horizontal")
		# Vertical movement
		self.pos.y += self.direction.y*speed*dt
		self.rect.y = round(self.pos.y)
		self.hitbox.centery = self.rect.centery
		self.collision("vertical")