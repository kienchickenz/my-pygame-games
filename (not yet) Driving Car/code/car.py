import pygame
from settings import *
from pygame.math import Vector2

class Car(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		# Image setup
		self.original_image = pygame.image.load("../graphics/car.png").convert_alpha()
		self.image = self.original_image
		self.rect  = self.image.get_rect(center=(640,360))
		# Move
		self.direction = Vector2(0,0)
		self.pos = Vector2(self.rect.center)
		self.speed = SPEED
		self.angle = 0
		self.rotation_speed = ROTATION_SPEED

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.direction.x = -1
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

	# def rotate(self):
	# 	if self.direction.x > 0:
	# 		self.angle -= self.rotation_speed
	# 	elif self.direction.x < 0:
	# 		self.angle += self.rotation_speed
	# 	self.image = pygame.transform.rotozoom(self.original_image,self.angle,0.25)
	# 	# self.rect = self.image.get_rect(center = self.rect.center)

	def move(self,dt):
		if self.direction.magnitude()!=0: self.direction = self.direction.normalize()
		self.pos += self.direction*self.speed*dt
		self.rect = (round(self.pos.x),round(self.pos.y))

	def update(self,dt):
		self.input()
		# self.rotate()
		self.move(dt)
