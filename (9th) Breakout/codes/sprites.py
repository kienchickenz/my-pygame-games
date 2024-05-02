import pygame,sys
from settings import *
from pygame.math import Vector2
from random import choice,randint

class Player(pygame.sprite.Sprite):
	def __init__(self,groups,surfacemaker):
		super().__init__(groups)
		self.screen = pygame.display.get_surface()
		# Image setup
		self.surfacemaker = surfacemaker
		self.image = surfacemaker.get_surf("player",(WINDOW_WIDTH//10,WINDOW_HEIGHT//20))
		self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH//2,WINDOW_HEIGHT-20))
		self.old_rect = self.rect.copy()
		# Move
		self.direction = Vector2(0,0)
		self.pos = Vector2(self.rect.topleft)
		self.speed = PLAYER_SPEED
		self.hearts = 3
		# Laser
		self.laser_amount = 1
		self.laser_image = pygame.image.load("../graphics/other/laser.png").convert_alpha()
		self.laser_rects  = []

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.direction.x = -1
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

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

	def check_hearts(self):
		if self.hearts <= 0: sys.exit()

	def display_laser(self):
		self.laser_rects = []
		if self.laser_amount > 0:
			divider_length = self.rect.width / (self.laser_amount + 1)
			for i in range(self.laser_amount):
				x = self.rect.left + (i + 1) * divider_length
				laser_rect = self.laser_image.get_rect(midbottom=(x,self.rect.top))
				self.laser_rects.append(laser_rect)
				for laser_rect in self.laser_rects:
					self.screen.blit(self.laser_image,laser_rect)

	def upgrade(self,upgrade_type):
		if upgrade_type == "speed":
			self.speed += 50
		if upgrade_type == "heart":
			self.hearts += 1
		if upgrade_type == "size":
			new_width = self.rect.width * 1.1
			self.image = self.surfacemaker.get_surf("player",(new_width,self.rect.height))
			self.rect  = self.image.get_rect(center=self.rect.center)
			self.pos.x = self.rect.x
		if upgrade_type == "laser":
			self.laser_amount += 1
 
	def update(self,dt):
		self.check_hearts()

		self.old_rect = self.rect.copy()
		self.input()
		self.move(dt)
		self.constraint()

		self.display_laser()

class Ball(pygame.sprite.Sprite):
	def __init__(self,groups,player,blocks):
		super().__init__(groups)
		# Image setup
		self.image = pygame.image.load("../graphics/other/ball.png").convert_alpha()
		self.rect  = self.image.get_rect(midbottom=player.rect.midtop)
		self.old_rect = self.rect.copy()
		# Move
		self.direction = Vector2(choice([1,-1]),-1)
		self.pos = Vector2(self.rect.topleft)
		self.speed = BALL_SPEED
		# Collision
		self.player = player
		self.blocks = blocks
		self.active = False
		# Music
		self.impact_sound = pygame.mixer.Sound("../musics/impact.ogg")
		self.impact_sound.set_volume(0.1)
		self.fail_sound = pygame.mixer.Sound("../musics/fail.ogg")
		self.fail_sound.set_volume(0.1)

	def window_collision(self,direction):
		if direction == "horizontal":
			if self.rect.right > WINDOW_WIDTH: 
				self.rect.right = WINDOW_WIDTH
				self.direction.x *= -1
				self.pos.x = self.rect.x
			elif self.rect.left < 0: 
				self.rect.left = 0
				self.direction.x *= -1
				self.pos.x = self.rect.x
		if direction == "vertical":
			if self.rect.top < 0:
				self.rect.top = 0
				self.direction.y *= -1
				self.pos.y = self.rect.y
			elif self.rect.top > WINDOW_HEIGHT:
				self.direction = Vector2(choice([1,-1]),-1)		
				self.active = False
				self.player.hearts -= 1
				self.fail_sound.play()

	def collision(self,direction):
		collision_sprites = pygame.sprite.spritecollide(self,self.blocks,False)
		if self.rect.colliderect(self.player.rect):
			collision_sprites.append(self.player)
		if collision_sprites:
			for sprite in collision_sprites:
				if direction == "horizontal":
					if self.rect.right >= sprite.rect.left:
						if self.old_rect.right <= sprite.old_rect.left:
							self.rect.right = sprite.rect.left - 1
							self.pos.x = self.rect.x
							self.direction.x *= -1
							self.impact_sound.play()
					if self.rect.left <= sprite.rect.right:
						if self.old_rect.left >= sprite.old_rect.right:
							self.rect.left = sprite.rect.right + 1
							self.pos.x = self.rect.x
							self.direction.x *= -1
							self.impact_sound.play()
					if getattr(sprite,"health",None):
						sprite.get_damage(1)

				elif direction == "vertical":
					if self.rect.top <= sprite.rect.bottom:
						if self.old_rect.top >= sprite.old_rect.bottom:
							self.rect.top = sprite.rect.bottom + 1
							self.pos.y = self.rect.y
							self.direction.y *= -1	
							self.impact_sound.play()				
					if self.rect.bottom >= sprite.rect.top:
						if self.old_rect.bottom <= sprite.old_rect.top:
							self.rect.bottom = sprite.rect.top - 1
							self.pos.y = self.rect.y
							self.direction.y *= -1
							self.impact_sound.play()
					if getattr(sprite,"health",None):
						sprite.get_damage(1)

	def move(self,dt):
		if self.active:
			if self.direction.magnitude()!=0: self.direction = self.direction.normalize()
			# Horizontal movement
			self.pos.x += self.direction.x*self.speed*dt
			self.rect.x = round(self.pos.x)
			self.collision("horizontal")
			self.window_collision("horizontal")
			# Vertical movement
			self.pos.y += self.direction.y*self.speed*dt
			self.rect.y = round(self.pos.y)
			self.collision("vertical")
			self.window_collision("vertical")
		else:
			self.rect.midbottom = self.player.rect.midtop
			self.pos = Vector2(self.rect.topleft)

	def update(self,dt):
		self.old_rect = self.rect.copy()
		self.move(dt)

class Block(pygame.sprite.Sprite):
	def __init__(self,groups,block_type,pos,surfacemaker,create_upgrade):
		super().__init__(groups)
		self.surfacemaker = surfacemaker
		self.image = surfacemaker.get_surf(COLOR_LEGEND[block_type],(BLOCK_WIDTH,BLOCK_HEIGHT))
		self.rect  = self.image.get_rect(topleft = pos)
		self.old_rect = self.rect.copy()
		self.health = int(block_type)
		self.create_upgrade = create_upgrade

	def get_damage(self,amount):
		self.health -= amount
		if self.health > 0:
			self.image = self.surfacemaker.get_surf(COLOR_LEGEND[str(self.health)],(BLOCK_WIDTH,BLOCK_HEIGHT))
		else:
			if randint(0,10) < 7: self.create_upgrade(self.rect.center)
			self.kill()

class Upgrade(pygame.sprite.Sprite):
	def __init__(self,groups,pos,upgrade_type):
		super().__init__(groups)
		# Image setup
		self.image = pygame.image.load(f"../graphics/upgrades/{upgrade_type}.png").convert_alpha()
		self.rect  = self.image.get_rect(midtop=pos)
		self.upgrade_type = upgrade_type
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.speed = UPGRADE_FALLING_SPEED

	def update(self,dt):
		self.pos.y += self.speed*dt
		self.rect.y = round(self.pos.y)

		if self.rect.top >= WINDOW_HEIGHT + 100: self.kill()

class Projectile(pygame.sprite.Sprite):
	def __init__(self,groups,pos,image):
		super().__init__(groups)
		# Image setup
		self.image = image
		self.rect  = self.image.get_rect(midbottom=pos)
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.speed = PROJECTILE_SPEED

	def move(self,dt):
		self.pos.y -= self.speed*dt
		self.rect.y = round(self.pos.y)

	def update(self,dt):
		self.move(dt)
		if self.rect.bottom <= -100: self.kill()