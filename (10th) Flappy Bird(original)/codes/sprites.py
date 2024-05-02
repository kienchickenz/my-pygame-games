import pygame
from settings import *
from pygame.math import Vector2
from random import randint

class Ground(pygame.sprite.Sprite):
	def __init__(self,groups,scale_image):
		super().__init__(groups)
		# Image setup
		ground_image = scale_image("../graphics/environment/ground.png")
		self.image = pygame.Surface((ground_image.get_width()*2,ground_image.get_height()))
		self.image.blit(ground_image,(0,0))
		self.image.blit(ground_image,(ground_image.get_width(),0))
		self.rect = self.image.get_rect(topleft=(0,615))
		self.z = LAYERS["Ground"]
		# Move
		self.pos = Vector2(self.rect.topleft)	
		self.direction = Vector2(-1,0)
		self.speed = 150
		self.sprite_type = "ground"
		# Collision
		self.mask = pygame.mask.from_surface(self.image)

	def move(self,dt):
		self.pos.x += self.direction.x*self.speed*dt
		if self.rect.centerx <= 0: self.pos.x = 0
		self.rect.x = round(self.pos.x)		

	def update(self,dt):
		self.move(dt)

class Bird(pygame.sprite.Sprite):
	def __init__(self,groups,scale_image):
		super().__init__(groups)
		# Image setup
		self.scale_image = scale_image
		self.image_list = self.import_images()
		self.image_index = 0
		self.animation_speed = 7
		self.image = self.image_list[self.image_index]
		self.rect  = self.image.get_rect(center=(WINDOW_WIDTH//10,WINDOW_HEIGHT/2))
		self.z = LAYERS["Main"]
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(0,0)
		self.gravity = 700
		self.jump_gravity = -400
		self.angle = 0
		# Collision
		self.maks = pygame.mask.from_surface(self.image)
		# Music
		self.flap_sound = pygame.mixer.Sound("../musics/wing.ogg")
		self.flap_sound.set_volume(0.2)

	def import_images(self):
		image_list = []
		for i in range(3):
			image = self.scale_image(f"../graphics/bird/yellow_{i}.png")
			image_list.append(image)
		return image_list

	def apply_gravity(self,dt):
		self.direction.y += self.gravity*dt
		self.pos.y += self.direction.y*dt
		self.rect.y = round(self.pos.y)

	def jump(self):
		self.direction.y = 0
		self.direction.y += self.jump_gravity
		self.flap_sound.play()

	def animate(self,dt):
		self.image_index += self.animation_speed*dt
		if self.image_index >= len(self.image_list): self.image_index = 0
		self.image = self.image_list[int(self.image_index)]

	def rotate(self):
		self.angle = -self.direction.y*0.09
		rotated_image = pygame.transform.rotozoom(self.image,self.angle,1)
		self.image = rotated_image
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.apply_gravity(dt)
		self.animate(dt)
		self.rotate()

class Pipe(pygame.sprite.Sprite):
	def __init__(self,groups,scale_image,pos,orientation):
		super().__init__(groups)
		# Image setup
		self.image = scale_image("../graphics/pipe/green.png")
		self.starting_point = pos
		offset = Vector2(0,75)
		if orientation == "up":
			self.starting_point = self.starting_point + offset
			self.rect = self.image.get_rect(midtop=self.starting_point)
		if orientation == "down":
			self.image = pygame.transform.rotozoom(self.image,180,1)
			self.starting_point = self.starting_point - offset
			self.rect = self.image.get_rect(midbottom=self.starting_point)
		self.z = LAYERS["Main"]
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(-1,0)
		self.speed = 300
		# Collision
		self.mask = pygame.mask.from_surface(self.image)
		self.sprite_type = "pipe"

	def move(self,dt):
		self.pos.x += self.direction.x*self.speed*dt
		self.rect.x = round(self.pos.x)
		if self.rect.right <= -100: self.kill()

	def update(self,dt):
		self.move(dt) 