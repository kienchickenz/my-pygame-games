import pygame
from settings import *
from entity   import Entity
from pygame.math import Vector2
class Monster:
	def get_player_distance_direction(self):
		enemy_pos  = Vector2(self.rect.center)
		player_pos = Vector2(self.player.rect.center)
		distance   = (player_pos - enemy_pos).magnitude()
		if distance!=0:
			direction = (player_pos - enemy_pos).normalize()
		else:
			direction = Vector2(0,0)
		return distance,direction

	def face_to_player(self):
		distance,direction = self.get_player_distance_direction()
		if distance < self.notice_radius:
			if -0.5 < direction.y < 0.5:
				if direction.x < 0:
					self.status = "left_idle"
				elif direction.x > 0:
					self.status = "right_idle"
			else:
				if direction.y < 0:
					self.status = "up_idle"
				elif direction.y > 0:
					self.status = "down_idle"

	def walk_to_player(self):
		distance,direction = self.get_player_distance_direction()
		if self.attack_radius < distance < self.walk_radius:
			self.direction = direction
			self.status = self.status.split("_")[0]
		else: 
			self.direction = Vector2(0,0)

class Coffin(Entity,Monster):
	def __init__(self,pos,groups,path,collision_sprites,player):
		super().__init__(pos,groups,path,collision_sprites)
		# Overwrites
		self.speed = 130
		# Player interation
		self.player = player
		self.notice_radius = 550
		self.walk_radius   = 400
		self.attack_radius = 50

	def attack(self):
		if not self.attacking:
			if self.get_player_distance_direction()[0] < self.attack_radius:
				self.attacking = True
				self.image_index = 0
		elif self.attacking:
			self.status = self.status.split("_")[0] + "_attack"

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += COFFIN_ANIMATION_SPEED*dt
		if int(self.image_index)==4 and self.attacking:
			if self.get_player_distance_direction()[0] < self.attack_radius:
				self.player.damage()
		if int(self.image_index) >= len(current_animation): 
			self.image_index = 0
			if self.attacking: self.attacking = False
		self.image = current_animation[int(self.image_index)]
		self.mask  = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.face_to_player()
		self.walk_to_player()
		self.attack()

		self.move(dt)
		self.animate(dt)
		self.blink()

		self.check_death()
		self.vulnerability_timer()

class Cactus(Entity,Monster):
	def __init__(self,pos,groups,path,collision_sprites,player,create_bullet):
		super().__init__(pos,groups,path,collision_sprites)
		# Overwrites
		self.speed = 100
		# Player interaction
		self.player = player
		self.notice_radius = 600
		self.walk_radius = 500
		self.attack_radius = 350
		# Bullet
		self.create_bullet = create_bullet
		self.bullet_shot = False

	def attack(self):
		if not self.attacking:
			if self.get_player_distance_direction()[0] < self.attack_radius:
				self.attacking = True
				self.bullet_shot = False
				self.image_index = 0
		elif self.attacking:
			self.status = self.status.split("_")[0] + "_attack"

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += CACTUS_ANIMATION_SPEED*dt
		if int(self.image_index) == 6 and self.attacking and not self.bullet_shot:
			self.bullet_shot = True
			self.bullet_direction = self.get_player_distance_direction()[1]
			bullet_start_pos = self.rect.center + self.bullet_direction*120
			if self.bullet_direction.y > 0: bullet_start_pos.x -= 20
			if self.bullet_direction.y < 0: bullet_start_pos.x += 20
			self.create_bullet(bullet_start_pos,self.bullet_direction)
			self.shoot_sound.play()
		if int(self.image_index) >= len(current_animation): 
			self.image_index = 0
			if self.attacking: 
				self.attacking = False
		self.image = current_animation[int(self.image_index)]		
		self.mask  = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.face_to_player()
		self.walk_to_player()
		self.attack()
		
		self.move(dt)
		self.animate(dt)
		self.blink()

		self.check_death()
		self.vulnerability_timer()