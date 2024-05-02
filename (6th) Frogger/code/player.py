import pygame,sys
from settings    import *
from pygame.math import Vector2
from os          import walk
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,collision_sprites):
		super().__init__(groups)
		self.import_image()
		self.image_index = 0
		self.status = "right"
		self.image  = self.animations[self.status][self.image_index]
		self.rect   = self.image.get_rect(center=pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height/2)
		self.pos = Vector2(self.rect.center)
		self.direction = Vector2((0,0))
		self.speed = PLAYER_SPEED
		self.collision_sprites = collision_sprites
	
	def detect_collision(self,direction):
		match direction:
			case "horizontal":
				for sprite in self.collision_sprites.sprites():
					if sprite.hitbox.colliderect(self.hitbox):
						if hasattr(sprite,"name") and sprite.name=="car":
							sys.exit()
						if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x        = self.hitbox.centerx
			case "vertical":
				for sprite in self.collision_sprites.sprites():
					if sprite.hitbox.colliderect(self.hitbox):
						if hasattr(sprite,"name") and sprite.name=="car":
							sys.exit()						
						if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y        = self.hitbox.centery

	def import_image(self):
		self.animations = {}
		for index,folder in enumerate(walk("../graphics/player")):
			if index == 0:
				for name in folder[1]:
					self.animations[name] = []
			else:
				for file_name in folder[2]:
					path  = folder[0].replace("\\","/") + "/" + file_name
					image = pygame.image.load(path).convert_alpha()
					key   = folder[0].split("\\")[1]
					self.animations[key].append(image)
	
	def update(self,dt):
		self.input()
		self.move(dt)
		self.animate(dt)
		self.restrict()
	
	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:  
			self.direction.x = -1
			self.status = "left"
		elif keys[pygame.K_RIGHT]: 
			self.direction.x = 1
			self.status = "right"
		else: 
			self.direction.x = 0
		if keys[pygame.K_UP]:    
			self.direction.y = -1
			self.status = "up"
		elif keys[pygame.K_DOWN]:  
			self.direction.y = 1
			self.status = "down"
		else:
			self.direction.y = 0
	
	def move(self,dt):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		self.pos.x += self.direction.x*self.speed*dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx   = round(self.pos.x)
		self.detect_collision("horizontal")
		self.pos.y += self.direction.y*self.speed*dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery   = round(self.pos.y)
		self.detect_collision("vertical")
	
	def animate(self,dt):
		current_animation = self.animations[self.status]
		if self.direction.magnitude()!=0:
			self.image_index += ANIMATION_SPEED*dt
			if self.image_index >= len(current_animation): self.image_index = 0
		else:
			self.image_index = 0
		self.image = current_animation[int(self.image_index)]

	def restrict(self):
		if self.rect.left < 640:
			self.pos.x = 640 + self.rect.width/2
			self.hitbox.left = 640
			self.rect.left   = 640
		if self.rect.right > 2560:
			self.pos.x = 2560 - self.rect.width/2
			self.hitbox.right = 2560
			self.rect.right   = 2560
		if self.rect.bottom > 3500:
			self.pos.y = 3500 - self.rect.height/2
			self.rect.bottom    = 3500
			self.hitbox.centery = self.rect.centery