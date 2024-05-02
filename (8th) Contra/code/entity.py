<<<<<<< HEAD
import pygame
from settings import *
from pygame.math import Vector2
from os   import walk
from math import sin
class Entity(pygame.sprite.Sprite):
	def __init__(self,pos,groups,path,create_bullet):
		super().__init__(groups)
		# Graphic setup
		self.import_image(path)
		self.image_index = 0
		self.status = "right"
		# Image setup
		self.image = self.animations[self.status][self.image_index]
		self.rect  = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()
		self.z = LAYERS["Main"]
		self.mask = pygame.mask.from_surface(self.image)
		# Move
		self.direction = Vector2(0,0)
		self.pos   = Vector2(self.rect.center)
		self.speed = PLAYER_SPEED
		self.duck = False
		# Attack
		self.create_bullet = create_bullet
		self.can_shoot = True
		self.shoot_time = 0
		self.cooldown = PLAYER_SHOOT_COOLDOWN
		# Health
		self.health = 3
		self.is_vulnerable = True
		self.hit_time = None
		# Music
		self.hit_sound = pygame.mixer.Sound("../audio/hit.ogg")
		self.hit_sound.set_volume(0.2)
		self.bullet_sound = pygame.mixer.Sound("../audio/bullet.ogg")
		self.bullet_sound.set_volume(0.2)

	def import_image(self,path):
		self.animations = {}
		for index,folder in enumerate(walk(path)):
			if index == 0:
				for name in folder[1]:
					self.animations[name] = []
			else:
				for file_name in sorted(folder[2],key=lambda string:int(string.split(".")[0])):
					path  = folder[0].replace("\\","/") + f"/{file_name}"
					image = pygame.image.load(path).convert_alpha()
					key   = folder[0].split("\\")[1]
					self.animations[key].append(image)

	def shoot(self):
		if self.can_shoot:
			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()
			bullet_direction = Vector2(1,0) if self.status.split("_")[0] == "right" else Vector2(-1,0)
			x_offset = bullet_direction.x * 60
			y_offset = -20 if not self.duck else 10
			offset = Vector2(x_offset,y_offset)
			self.create_bullet(self.rect.center+offset,bullet_direction,self)
			self.bullet_sound.play()

	def shoot_cooldown(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > self.cooldown:
				self.can_shoot = True

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

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += ANIMATION_SPEED*dt
		if int(self.image_index) >= len(current_animation): self.image_index = 0
		self.image = current_animation[int(self.image_index)]
=======
import pygame
from settings import *
from pygame.math import Vector2
from os   import walk
from math import sin
class Entity(pygame.sprite.Sprite):
	def __init__(self,pos,groups,path,create_bullet):
		super().__init__(groups)
		# Graphic setup
		self.import_image(path)
		self.image_index = 0
		self.status = "right"
		# Image setup
		self.image = self.animations[self.status][self.image_index]
		self.rect  = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()
		self.z = LAYERS["Main"]
		self.mask = pygame.mask.from_surface(self.image)
		# Move
		self.direction = Vector2(0,0)
		self.pos   = Vector2(self.rect.center)
		self.speed = PLAYER_SPEED
		self.duck = False
		# Attack
		self.create_bullet = create_bullet
		self.can_shoot = True
		self.shoot_time = 0
		self.cooldown = PLAYER_SHOOT_COOLDOWN
		# Health
		self.health = 3
		self.is_vulnerable = True
		self.hit_time = None
		# Music
		self.hit_sound = pygame.mixer.Sound("../audio/hit.ogg")
		self.hit_sound.set_volume(0.2)
		self.bullet_sound = pygame.mixer.Sound("../audio/bullet.ogg")
		self.bullet_sound.set_volume(0.2)

	def import_image(self,path):
		self.animations = {}
		for index,folder in enumerate(walk(path)):
			if index == 0:
				for name in folder[1]:
					self.animations[name] = []
			else:
				for file_name in sorted(folder[2],key=lambda string:int(string.split(".")[0])):
					path  = folder[0].replace("\\","/") + f"/{file_name}"
					image = pygame.image.load(path).convert_alpha()
					key   = folder[0].split("\\")[1]
					self.animations[key].append(image)

	def shoot(self):
		if self.can_shoot:
			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()
			bullet_direction = Vector2(1,0) if self.status.split("_")[0] == "right" else Vector2(-1,0)
			x_offset = bullet_direction.x * 60
			y_offset = -20 if not self.duck else 10
			offset = Vector2(x_offset,y_offset)
			self.create_bullet(self.rect.center+offset,bullet_direction,self)
			self.bullet_sound.play()

	def shoot_cooldown(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > self.cooldown:
				self.can_shoot = True

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

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += ANIMATION_SPEED*dt
		if int(self.image_index) >= len(current_animation): self.image_index = 0
		self.image = current_animation[int(self.image_index)]
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
		self.mask = pygame.mask.from_surface(self.image)