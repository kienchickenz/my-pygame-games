import pygame,sys
from settings import *
from entity   import Entity
from pygame.math import Vector2
class Player(Entity):
	def __init__(self,pos,groups,path,collision_sprites,create_bullet):
		super().__init__(pos,groups,path,collision_sprites)
		# Bullet
		self.create_bullet = create_bullet
		self.bullet_shot = False
		self.bullet_direction = Vector2(0,0)

	def check_death(self):
		if self.health <= 0: sys.exit()

	def update(self,dt):
		self.input()
		self.get_status() 

		self.move(dt)
		self.animate(dt)
		self.blink()

		self.vulnerability_timer()
		self.check_death()

	def input(self):
		keys = pygame.key.get_pressed()
		if not self.attacking:
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
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.bullet_shot = False
				self.direction = Vector2(0,0)
				self.image_index = 0
				match self.status.split("_")[0]:
					case "left" : self.bullet_direction = Vector2(-1,0)
					case "right": self.bullet_direction = Vector2(1,0)
					case "up"   : self.bullet_direction = Vector2(0,-1)
					case "down" : self.bullet_direction = Vector2(0,1)

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += ANIMATION_SPEED*dt
		if int(self.image_index) == 2 and self.attacking and not self.bullet_shot:
			self.bullet_shot = True
			bullet_start_pos = self.rect.center + self.bullet_direction*80
			if self.bullet_direction.y > 0: bullet_start_pos.x -= 20
			if self.bullet_direction.y < 0: bullet_start_pos.x += 20
			self.create_bullet(bullet_start_pos,self.bullet_direction)
			self.shoot_sound.play()
		if int(self.image_index) >= len(current_animation): 
			self.image_index = 0
			if self.attacking: self.attacking = False
		self.image = current_animation[int(self.image_index)]
		self.mask  = pygame.mask.from_surface(self.image)

	def get_status(self):
		if self.direction.x==0 and self.direction.y==0:
			self.status = self.status.split("_")[0] + "_idle"
		if self.attacking:
			self.status = self.status.split("_")[0] + "_attack"