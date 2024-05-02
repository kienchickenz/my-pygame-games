<<<<<<< HEAD
import pygame
from settings import *
from entity   import Entity
from pygame.math import Vector2
class Enemy(Entity):
	def __init__(self,pos,groups,path,create_bullet,player,collision_sprites):
		super().__init__(pos,groups,path,create_bullet)
		self.player = player
		for sprite in collision_sprites.sprites():
			if sprite.rect.collidepoint(self.rect.midbottom):
				self.rect.midbottom = sprite.rect.midtop
		# Overwrites
		self.cooldown = ENEMY_SHOOT_COOLDOWN

	def get_status(self):
		if self.player.rect.centerx < self.rect.centerx:
			self.status = "left"
		else:
			self.status = "right"

	def check_fire(self):
		enemy_pos  = Vector2(self.rect.center)
		player_pos = Vector2(self.player.rect.center)
		distance = (player_pos - enemy_pos).magnitude()
		same_y = False
		if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20:
			same_y = True 
		if distance < ATTACK_RADIUS and same_y: self.shoot()

	def update(self,dt):
		self.get_status()
		self.animate(dt)
		self.blink()

		self.check_fire()
		self.shoot_cooldown()

		self.check_death()
=======
import pygame
from settings import *
from entity   import Entity
from pygame.math import Vector2
class Enemy(Entity):
	def __init__(self,pos,groups,path,create_bullet,player,collision_sprites):
		super().__init__(pos,groups,path,create_bullet)
		self.player = player
		for sprite in collision_sprites.sprites():
			if sprite.rect.collidepoint(self.rect.midbottom):
				self.rect.midbottom = sprite.rect.midtop
		# Overwrites
		self.cooldown = ENEMY_SHOOT_COOLDOWN

	def get_status(self):
		if self.player.rect.centerx < self.rect.centerx:
			self.status = "left"
		else:
			self.status = "right"

	def check_fire(self):
		enemy_pos  = Vector2(self.rect.center)
		player_pos = Vector2(self.player.rect.center)
		distance = (player_pos - enemy_pos).magnitude()
		same_y = False
		if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20:
			same_y = True 
		if distance < ATTACK_RADIUS and same_y: self.shoot()

	def update(self,dt):
		self.get_status()
		self.animate(dt)
		self.blink()

		self.check_fire()
		self.shoot_cooldown()

		self.check_death()
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
		self.vulnerability_timer()