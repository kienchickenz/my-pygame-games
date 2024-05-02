import pygame,sys
from settings import *
from pygame.math import Vector2
from math import sin

class Player(pygame.sprite.Sprite):
	def __init__(self,groups,image,pos,create_laser):
		super().__init__(groups)
		# Image
		self.player_image = image
		self.image = self.player_image
		self.rect  = self.image.get_rect(midbottom=pos)
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(0,0)
		self.speed = 300
		# Shoot
		self.can_shoot = True
		self.shoot_time = 0
		self.shoot_cooldown = 600
		self.create_laser = create_laser
		# Collision
		self.mask = pygame.mask.from_surface(self.image)
		# Health
		self.lives = 3
		self.is_vulnerable = True
		self.vulnerability_time = 700
		self.hit_time = 0

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE]:
			if self.can_shoot: self.shoot()

	def move(self,dt):
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.x = round(self.pos.x)

	def constraint(self):
		if self.rect.left < 0:
			self.rect.left = 0
			self.pos.x = self.rect.x
		elif self.rect.right > WINDOW_WIDTH:
			self.rect.right = WINDOW_WIDTH
			self.pos.x = self.rect.x

	def shoot_timer(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > self.shoot_cooldown: 
				self.can_shoot = True

	def shoot(self):
		self.can_shoot = False
		self.shoot_time = pygame.time.get_ticks()
		offset = Vector2(0,-5)
		self.create_laser(self.rect.midtop + offset,"Player")

	def damage(self):
		if self.is_vulnerable:
			self.lives -= 1
			self.is_vulnerable = False
			self.hit_time = pygame.time.get_ticks()

	def check_death(self):
		if self.lives <= 0: sys.exit()

	def vulnerability_timer(self):
		if not self.is_vulnerable:
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > self.vulnerability_time:
				self.is_vulnerable = True

	def blink(self):
		if not self.is_vulnerable:
			if self.wave_value():
				mask = pygame.mask.from_surface(self.image)
				white_surface = mask.to_surface()
				white_surface.set_colorkey("black")
				self.image = white_surface

	def wave_value(self):
		wave = sin(pygame.time.get_ticks())
		if wave >= 0: return True
		return False

	def animate(self):
		self.image = self.player_image

	def update(self,dt):
		self.input()
		self.move(dt)
		self.constraint()

		self.animate()
		self.blink()

		self.shoot_timer()
		self.check_death()

		self.vulnerability_timer()

class Laser(pygame.sprite.Sprite):
	def __init__(self,groups,pos,entity):
		super().__init__(groups)
		# Image
		self.image = pygame.Surface((4,20))
		self.rect  = self.image.get_rect(center=pos)
		self.image.fill("white")
		# Move
		self.pos = Vector2(self.rect.topleft)
		if entity == "Alien":
			self.direction = Vector2(0,1)
		elif entity == "Player":
			self.direction = Vector2(0,-1)
		self.speed = 350

	def move(self,dt):
		self.pos.y += self.direction.y*self.speed*dt
		self.rect.y = round(self.pos.y)

	def update(self,dt):
		self.move(dt)
		if self.rect.y <= -100 or self.rect.y >= 100 + WINDOW_HEIGHT:
			self.kill()

class Block(pygame.sprite.Sprite):
	def __init__(self,groups,pos):
		super().__init__(groups)
		self.image = pygame.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.rect  = self.image.get_rect(topleft=(pos))
		self.image.fill((120,120,120))

class Alien(pygame.sprite.Sprite):
	def __init__(self,groups,color,pos):
		super().__init__(groups)
		# Image setup
		self.image = pygame.image.load(f"../graphics/alien/{color}.png").convert_alpha()
		self.rect  = self.image.get_rect(topleft=pos)
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.speed = 70
		# Collision
		self.mask = pygame.mask.from_surface(self.image)
		# Score
		match color:
			case "yellow":
				self.value = 300
			case "green":
				self.value = 200
			case "red":
				self.value = 100

	def move(self,dt,direction):
		# Horizontal movement
		self.pos.x += direction.x*self.speed*dt
		self.rect.x = round(self.pos.x)
		# Vertical movement
		self.pos.y += direction.y*self.speed*dt
		self.rect.y = round(self.pos.y)

class ExtraAlien(pygame.sprite.Sprite):
	def __init__(self,groups,side):
		super().__init__(groups)
		if side == "right":
			rect_x = WINDOW_WIDTH + 50
			direction_x = -1
		elif side == "left":
			rect_x = -50
			direction_x = 1
		# Image setup
		self.image = pygame.image.load("../graphics/alien/extra.png").convert_alpha()
		self.rect  = self.image.get_rect(topleft=(rect_x,80))
		# Move
		self.direction = Vector2(direction_x,0)
		self.pos = Vector2(self.rect.topleft)
		self.speed = 200
		# Collision
		self.mask = pygame.mask.from_surface(self.image)

	def move(self,dt):
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.x = round(self.pos.x)

	def update(self,dt):
		self.move(dt)
		if self.rect.x > WINDOW_WIDTH + 100 or self.rect.x < -100:
			self.kill()