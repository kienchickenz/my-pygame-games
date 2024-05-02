import pygame
from settings import *
from pygame.math import Vector2
from random import choice

class Player(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		# Image setup
		self.image = pygame.Surface((WINDOW_WIDTH//10,WINDOW_HEIGHT//20))
		self.image.fill("orange")
		self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH//2,WINDOW_HEIGHT-20))
		# Move
		self.direction = Vector2(0,0)
		self.pos = Vector2(self.rect.topleft)
		self.speed = PLAYER_SPEED

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
		if self.rect.left <= 0:
			self.rect.left = 0
		elif self.rect.right >= WINDOW_WIDTH:
			self.rect.right = WINDOW_WIDTH
		self.pos.x = self.rect.x

	def update(self,dt):
		self.input()
		self.move(dt)
		self.constraint()

class Ball(pygame.sprite.Sprite):
	def __init__(self,groups,player):
		super().__init__(groups)
		# Image setup
		self.image = pygame.image.load("../graphics/other/ball.png").convert_alpha()
		self.rect  = self.image.get_rect(midbottom=player.rect.midtop)
		# Move
		self.direction = Vector2(choice([1,-1]),-1)
		self.pos = Vector2(self.rect.topleft)
		self.speed = BALL_SPEED
		# Collision
		self.player = player
		self.active = False

	def start(self):
		keys = pygame.key.get_pressed()
		if not self.active:
			if keys[pygame.K_SPACE]: self.active = True

	def move(self,dt):
		if self.active:
			if self.direction.magnitude()!=0: self.direction = self.direction.normalize()
			# Horizontal movement
			self.pos += self.direction*self.speed*dt
			self.rect.x = round(self.pos.x)
			print(self.pos)

			# Vertical movement
			self.pos.y += self.direction.y*self.speed*dt
			self.rect.y = round(self.pos.y)

		else:
			self.rect.midbottom = self.player.rect.midtop
			self.pos = self.rect.topleft

	def update(self,dt):
		self.start()
		self.move(dt)