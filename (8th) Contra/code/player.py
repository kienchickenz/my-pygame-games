<<<<<<< HEAD
import pygame,sys
from settings import *
from entity   import Entity
from pygame.math import Vector2
class Player(Entity):
	def __init__(self,pos,groups,path,collision_sprite,create_bullet):
		super().__init__(pos,groups,path,create_bullet)
		# Collision
		self.collision_sprite = collision_sprite
		self.moving_floor = None
		# Vertical movement
		self.gravity = GRAVITY
		self.jump_speed = JUMP_SPEED
		self.on_floor = False
		# Overwrites
		self.health = 10

	def get_status(self):
		if self.on_floor:
			if self.direction.x == 0:
				self.status = self.status.split("_")[0] + "_idle"
			if self.duck:
				self.status = self.status.split("_")[0] + "_duck"
		else:
			self.status = self.status.split("_")[0] + "_jump"

	def check_contact(self):
		bottom_rect = pygame.Rect((0,0),(self.rect.width,5))
		bottom_rect.midtop = self.rect.midbottom
		for sprite in self.collision_sprite.sprites():
			if sprite.rect.colliderect(bottom_rect):
				if self.direction.y > 0:
					self.on_floor = True
				if hasattr(sprite,"direction"):
					self.moving_floor = sprite

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
		if keys[pygame.K_UP] and self.on_floor:	
			self.direction.y = -self.jump_speed
		self.duck = False
		if keys[pygame.K_DOWN] : self.duck = True
		if keys[pygame.K_SPACE]: self.shoot()

	def detect_collision(self,direction):
		for sprite in self.collision_sprite.sprites():
			if sprite.rect.colliderect(self.rect):
				if direction == "horizontal":
					if self.rect.left <= sprite.rect.right:
						if self.old_rect.left >= sprite.old_rect.right:
							self.rect.left = sprite.rect.right
					if self.rect.right >= sprite.rect.left:
						if self.old_rect.right <= sprite.old_rect.left:
							self.rect.right = sprite.rect.left
					self.pos.x = self.rect.centerx
				elif direction == "vertical":
					if self.rect.top <= sprite.rect.bottom:
						if self.old_rect.top >= sprite.old_rect.bottom:
							self.rect.top = sprite.rect.bottom
					if self.rect.bottom >= sprite.rect.top:
						if self.old_rect.bottom <= sprite.old_rect.top:
							self.rect.bottom = sprite.rect.top
							self.on_floor = True
					self.pos.y = self.rect.centery
					self.direction.y = 0
		if self.on_floor and self.direction.y != 0:
			self.on_floor = False

	def move(self,dt):
		if self.duck and self.on_floor: self.direction.x = 0
		# Horizontal movement
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.centerx = round(self.pos.x)
		self.detect_collision("horizontal")
		# Vertical movement
		self.direction.y += self.gravity
		self.pos.y += self.direction.y*dt
		self.rect.centery = round(self.pos.y)
		self.detect_collision("vertical")
		# Glue player to the floor
		if self.moving_floor and self.moving_floor.direction.y > 0: 
			if self.direction.y > 0:
				self.on_floor = True
				self.direction.y = 0
				self.rect.bottom = self.moving_floor.rect.top
				self.pos.y = self.rect.centery
		self.moving_floor = None

	def check_death(self):
		if self.health <= 0: sys.exit()

	def update(self,dt):
		self.input()
		self.get_status()

		self.old_rect = self.rect.copy()
		self.move(dt)
		self.check_contact()
		self.animate(dt)
		self.blink()

		self.shoot_cooldown()

		self.check_death()
=======
import pygame,sys
from settings import *
from entity   import Entity
from pygame.math import Vector2
class Player(Entity):
	def __init__(self,pos,groups,path,collision_sprite,create_bullet):
		super().__init__(pos,groups,path,create_bullet)
		# Collision
		self.collision_sprite = collision_sprite
		self.moving_floor = None
		# Vertical movement
		self.gravity = GRAVITY
		self.jump_speed = JUMP_SPEED
		self.on_floor = False
		# Overwrites
		self.health = 10

	def get_status(self):
		if self.on_floor:
			if self.direction.x == 0:
				self.status = self.status.split("_")[0] + "_idle"
			if self.duck:
				self.status = self.status.split("_")[0] + "_duck"
		else:
			self.status = self.status.split("_")[0] + "_jump"

	def check_contact(self):
		bottom_rect = pygame.Rect((0,0),(self.rect.width,5))
		bottom_rect.midtop = self.rect.midbottom
		for sprite in self.collision_sprite.sprites():
			if sprite.rect.colliderect(bottom_rect):
				if self.direction.y > 0:
					self.on_floor = True
				if hasattr(sprite,"direction"):
					self.moving_floor = sprite

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
		if keys[pygame.K_UP] and self.on_floor:	
			self.direction.y = -self.jump_speed
		self.duck = False
		if keys[pygame.K_DOWN] : self.duck = True
		if keys[pygame.K_SPACE]: self.shoot()

	def detect_collision(self,direction):
		for sprite in self.collision_sprite.sprites():
			if sprite.rect.colliderect(self.rect):
				if direction == "horizontal":
					if self.rect.left <= sprite.rect.right:
						if self.old_rect.left >= sprite.old_rect.right:
							self.rect.left = sprite.rect.right
					if self.rect.right >= sprite.rect.left:
						if self.old_rect.right <= sprite.old_rect.left:
							self.rect.right = sprite.rect.left
					self.pos.x = self.rect.centerx
				elif direction == "vertical":
					if self.rect.top <= sprite.rect.bottom:
						if self.old_rect.top >= sprite.old_rect.bottom:
							self.rect.top = sprite.rect.bottom
					if self.rect.bottom >= sprite.rect.top:
						if self.old_rect.bottom <= sprite.old_rect.top:
							self.rect.bottom = sprite.rect.top
							self.on_floor = True
					self.pos.y = self.rect.centery
					self.direction.y = 0
		if self.on_floor and self.direction.y != 0:
			self.on_floor = False

	def move(self,dt):
		if self.duck and self.on_floor: self.direction.x = 0
		# Horizontal movement
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.centerx = round(self.pos.x)
		self.detect_collision("horizontal")
		# Vertical movement
		self.direction.y += self.gravity
		self.pos.y += self.direction.y*dt
		self.rect.centery = round(self.pos.y)
		self.detect_collision("vertical")
		# Glue player to the floor
		if self.moving_floor and self.moving_floor.direction.y > 0: 
			if self.direction.y > 0:
				self.on_floor = True
				self.direction.y = 0
				self.rect.bottom = self.moving_floor.rect.top
				self.pos.y = self.rect.centery
		self.moving_floor = None

	def check_death(self):
		if self.health <= 0: sys.exit()

	def update(self,dt):
		self.input()
		self.get_status()

		self.old_rect = self.rect.copy()
		self.move(dt)
		self.check_contact()
		self.animate(dt)
		self.blink()

		self.shoot_cooldown()

		self.check_death()
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
		self.vulnerability_timer()