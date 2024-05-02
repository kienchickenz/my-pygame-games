import pygame
from pygame.math import Vector2

from settings import *
from sprites  import Generic
from timer    import Timer

from random import choice

class Spikes(Generic):
	def __init__(self,groups,pos,image):
		super().__init__(groups,pos,image)
		self.mask = pygame.mask.from_surface(self.image)

class Tooth(Generic):
	def __init__(self,groups,pos,images,collision_sprites):
		# Animation
		self.animation = images
		self.orientation = "right"
		self.image_index = 0
		image = self.animation[f"run_{self.orientation}"][self.image_index]
		super().__init__(groups,pos,image)
		self.rect.midbottom = self.rect.topleft + Vector2(TILE_SIZE/2,TILE_SIZE)
		self.mask = pygame.mask.from_surface(self.image)
		# Movement
		self.direction = Vector2(choice([1,-1]),0)
		self.orientation = "right" if self.direction.x > 0 else "left"
		self.pos = Vector2(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites
		# Destroy tooth at the beginning if he is not on a floor
		if not [sprite for sprite in collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + Vector2(0,10))]:
			self.kill()

	def animate(self,dt):
		current_animation = self.animation[f"run_{self.orientation}"]
		self.image_index += ANIMATION_SPEED * dt
		if self.image_index > len(current_animation): self.image_index = 0
		self.image = current_animation[int(self.image_index)]
		self.mask = pygame.mask.from_surface(self.image)

	def move(self,dt):
		right_gap = self.rect.bottomright + Vector2(1,1)
		right_block = self.rect.midright + Vector2(1,0)
		left_gap = self.rect.bottomleft + Vector2(-1,1)
		left_block = self.rect.midleft + Vector2(-1,0)
		if self.direction.x > 0: # Right
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_gap)]
			wall_sprites  = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_block)]
			if not floor_sprites or wall_sprites:
				self.direction.x = -1
				self.orientation = "left"
		if self.direction.x < 0: # Left
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_gap)]
			wall_sprites  = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_block)]
			if not floor_sprites or wall_sprites:
				self.direction.x = 1
				self.orientation = "right"
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)

	def update(self,dt):
		self.animate(dt)
		self.move(dt)

class Shell(Generic):
	def __init__(self,groups,pos,images,orientation,pearl_image,damage_sprites):
		self.orientation = orientation
		self.animation = images.copy()
		if orientation == "right":
			for key,value in self.animation.items():
				self.animation[key] = [pygame.transform.flip(image,True,False) 
										for image in value]
		self.image_index = 0
		self.status = "idle"
		super().__init__(groups,pos,self.animation[self.status][self.image_index])
		self.rect.bottom = self.rect.top + TILE_SIZE
		# Attack
		self.damage_sprites = damage_sprites
		self.pearl_image = pearl_image
		self.has_shot = False
		self.attack_cooldown = Timer(2000)

	def animate(self,dt):
		current_animation = self.animation[self.status]
		self.image_index += ANIMATION_SPEED * dt
		if self.image_index >= len(current_animation): 
			self.image_index = 0
			if self.has_shot:
				self.attack_cooldown.activate()
				self.has_shot = False
		self.image = current_animation[int(self.image_index)]
		if int(self.image_index) == 2:
			if self.status == "attack" and not self.has_shot:
				pearl_direction = Vector2(-1,0) if self.orientation == "left" else Vector2(1,0)
				offset = (pearl_direction * 50) + Vector2(0,-10) if self.orientation == "left" else (pearl_direction*20) + Vector2(0,-10)
				Pearl([self.groups()[0],self.damage_sprites],self.rect.center+offset,self.pearl_image,pearl_direction)
				self.has_shot = True

	def get_status(self):
		distance = Vector2(self.player.rect.center).distance_to(Vector2(self.rect.center))
		if distance < 500 and not self.attack_cooldown.active:
			self.status = "attack" 
		else:
			self.status = "idle"

	def update(self,dt):
		self.get_status()
		self.animate(dt)
		self.attack_cooldown.update()

class Pearl(Generic):
	def __init__(self,groups,pos,image,direction):
		super().__init__(groups,pos,image)
		self.mask = pygame.mask.from_surface(self.image)
		# Movement
		self.pos = Vector2(self.rect.topleft)
		self.direction = direction
		self.speed = 180

		self.timer = Timer(10000)
		self.timer.activate()

	def move(self,dt):
		self.pos.x += self.speed * self.direction.x * dt
		self.rect.x = round(self.pos.x)

	def update(self,dt):
		self.move(dt) 
		self.timer.update()
		if not self.timer.active: self.kill()