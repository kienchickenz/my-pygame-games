import pygame
from pygame.math import Vector2
from os import walk

class Player(pygame.sprite.Sprite):
	def __init__(self,groups,pos,collision_sprites):
		super().__init__(groups)
		# Animation
		self.animations = self.import_images("../graphic/player")
		self.status = "idle"
		self.facing_direction = "right"
		self.image_index = 0
		self.animation_speed = 7
		# Image
		self.image = self.animations[self.status][self.image_index]
		self.rect = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(0,0) 
		self.speed = 250
		# Jump
		self.gravity = 25
		self.jump_speed = 700
		self.on_floor = True
		# Collision
		self.collision_sprites = collision_sprites

	def import_images(self,path):
		animations = {}
		for index,folder in enumerate(walk(path)):
			if index == 0:
				for key in folder[1]:
					animations[key] = []
			else:
				for file_name in folder[2]:
					path = folder[0].replace("\\","/") + f"/{file_name}"
					image = pygame.image.load(path).convert_alpha()
					key = folder[0].split("\\")[1]
					animations[key].append(image)
		return animations
	
	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_direction = "left"
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_direction = "right"
		else:
			self.direction.x = 0
		if keys[pygame.K_SPACE] and self.on_floor:
			self.direction.y = -self.jump_speed

	def collision(self,direction):
		for sprite in self.collision_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if direction == "horizontal":
					if self.rect.left <= sprite.rect.right:
						if self.old_rect.left >= sprite.old_rect.right:
							self.rect.left = sprite.rect.right
					if self.rect.right >= sprite.rect.left:
						if self.old_rect.right <= sprite.rect.left:
							self.rect.right = sprite.rect.left
					self.pos.x = self.rect.x
				elif direction == "vertical":
					if self.rect.top <= sprite.rect.bottom:
						if self.old_rect.top >= sprite.rect.bottom:
							self.rect.top = sprite.rect.bottom
					if self.rect.bottom >= sprite.rect.top:
						if self.old_rect.bottom <= sprite.rect.top:
							self.rect.bottom = sprite.rect.top
							self.on_floor = True
					self.pos.y = self.rect.y
					self.direction.y = 0

	def move(self,dt):
		# Horizontal movement
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.x = round(self.pos.x)
		self.collision("horizontal")
		# Vertical movement
		self.direction.y += self.gravity
		self.pos.y += self.direction.y*dt
		self.rect.y = round(self.pos.y)
		self.collision("vertical")

	def get_status(self):
		if self.direction.y < 0:
			self.status = "jump"
			self.on_floor = False
		elif self.direction.y > 60:
			self.status = "fall"
			self.on_floor = False
		if self.on_floor:
			if self.direction.x != 0:
				self.status = "run"
			else:
				self.status = "idle"

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += self.animation_speed*dt
		if self.image_index >= len(current_animation): self.image_index = 0
		image = current_animation[int(self.image_index)]
		match self.facing_direction:
			case "right":
				self.image = image
			case "left":
				flipped_image = pygame.transform.flip(image,flip_x=True,flip_y=False)
				self.image = flipped_image

	def update(self,dt):
		self.old_rect = self.rect.copy()
		self.input()
		self.move(dt)
		self.get_status()
		self.animate(dt)