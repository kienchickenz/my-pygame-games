import pygame
from settings import *
from os       import walk
from math     import sin
from pygame.math import Vector2
class Entity(pygame.sprite.Sprite):
	def __init__(self,pos,groups,path,collision_sprites):
		super().__init__(groups)
		# Animate
		self.import_image(path)
		self.image_index = 0
		self.status = "down_idle"
		# Default
		self.image = self.animations[self.status][self.image_index]
		self.rect  = self.image.get_rect(center=(pos))
		# Move
		self.pos = Vector2(self.rect.center)
		self.direction = Vector2(0,0)
		self.speed = SPEED
		# Collision
		self.mask = pygame.mask.from_surface(self.image)
		self.hitbox = self.rect.inflate(-self.rect.width*0.5,-self.rect.height/2)
		self.collision_sprites = collision_sprites
		# Attack
		self.attacking = False
		# Health
		self.health = 3
		self.is_vulnerable = True
		self.hit_time = None
		# Sound
		self.hit_sound = pygame.mixer.Sound("../musics/hit.ogg")
		self.hit_sound.set_volume(0.3)
		self.shoot_sound = pygame.mixer.Sound("../musics/bullet.ogg")
		self.shoot_sound.set_volume(0.3)

	def import_image(self,path):
		self.animations = {}
		for index,folder in enumerate(walk(path)):
			if index==0:
				for name in folder[1]:
					self.animations[name] = []
			else:
				for file_name in sorted(folder[2],key=lambda string:int(string.split(".")[0])):
					path  = folder[0].replace("\\","/")+"/"+file_name
					image = pygame.image.load(path).convert_alpha()
					key   = folder[0].split("\\")[1]
					self.animations[key].append(image)

	def move(self,dt):
		if self.direction.magnitude()!=0:
			self.direction = self.direction.normalize()
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.centerx,self.hitbox.centerx = round(self.pos.x),round(self.pos.x)
		self.detect_collision("horizontal")
		self.pos.y += self.direction.y*self.speed*dt
		self.rect.centery,self.hitbox.centery = round(self.pos.y),round(self.pos.y)
		self.detect_collision("vertical")

	def detect_collision(self,direction):
		for sprite in self.collision_sprites.sprites():
			if self.hitbox.colliderect(sprite.hitbox):
				if direction=="horizontal":
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					elif self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx,self.pos.x = self.hitbox.centerx,self.hitbox.centerx
				elif direction=="vertical":
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					elif self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery,self.pos.y = self.hitbox.centery,self.hitbox.centery

	def damage(self):
		if self.is_vulnerable:
			self.is_vulnerable = False
			self.health -= 1
			self.hit_time = pygame.time.get_ticks()
			self.hit_sound.play()

	def check_death(self):
		if self.health <= 0: self.kill()

	def vulnerability_timer(self):
		if not self.is_vulnerable:
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > VULNERABILITY_TIME:
				self.is_vulnerable = True

	def blink(self):
		if not self.is_vulnerable:
			if self.wave_value():
				mask = pygame.mask.from_surface(self.image)
				white_surface = mask.to_surface()
				white_surface.set_colorkey("black")
				self.image = white_surface

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return True
		return False