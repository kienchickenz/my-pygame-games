import pygame
from settings import *
from timer    import Timer

from random import randint,choice
from pygame.math import Vector2

class Generic(pygame.sprite.Sprite):
	def __init__(self,groups,pos,image,z=LAYERS["main"]):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width*0.2,-self.rect.height*0.75)
		self.z = z

class Interaction(Generic):
	def __init__(self,groups,size,pos,name):
		image = pygame.Surface(size)
		super().__init__(groups,pos,image)
		self.name = name

class Water(Generic):
	def __init__(self,groups,pos,images):
		self.animation = images
		self.image_index = 0
		self.animation_speed = 7
		super().__init__(groups,pos,self.animation[self.image_index],LAYERS["water"])

	def animate(self,dt):
		self.image_index += self.animation_speed * dt
		if self.image_index >= len(self.animation): self.image_index = 0
		self.image = self.animation[int(self.image_index)]

	def update(self,dt):
		self.animate(dt)

class WildFlower(Generic):
	def __init__(self,groups,pos,image):
		super().__init__(groups,pos,image)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height*0.9)

class Tree(Generic):
	def __init__(self,groups,pos,image,name,add_inventory):
		super().__init__(groups,pos,image)
		self.health = 5
		self.alive = True
		stump_type = "small" if name == "Small" else "large"
		self.stump_image = pygame.image.load(f"../graphics/stumps/{stump_type}.png").convert_alpha()
		# Apples
		self.apple_image = pygame.image.load("../graphics/fruit/apple.png").convert_alpha()
		self.apple_pos = APPLE_POS[name]
		self.apple_sprites = pygame.sprite.Group()
		self.create_fruit()
		self.add_inventory = add_inventory
		# Sound
		self.axe_sound = pygame.mixer.Sound("../music/axe.ogg")

	def create_fruit(self):
		for pos in self.apple_pos:
			if randint(0,10) < 2:
				pos = self.rect.topleft + Vector2(pos)
				Generic([self.apple_sprites,self.groups()[0]],pos,self.apple_image,LAYERS["fruit"])

	def damage(self):
		if self.alive: 
			self.axe_sound.play()
			self.health -= 1
		if len(self.apple_sprites):
			random_apple = choice(self.apple_sprites.sprites())
			self.add_inventory("apple")
			random_apple.kill()
			Particle(self.groups()[0],random_apple.rect.topleft,random_apple.image,LAYERS["fruit"])

	def check_death(self):
		if self.health <= 0:
			self.alive = False
			self.add_inventory("wood")
			Particle(self.groups()[0],self.rect.topleft,self.image,LAYERS["fruit"],300)
			self.image = self.stump_image
			self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height)

	def update(self,dt):
		if self.alive: self.check_death()

class Particle(Generic):
	def __init__(self,groups,pos,image,z,duration=200):
		super().__init__(groups,pos,image,z)
		self.duration = Timer(duration)
		self.duration.activate()
		# White surface
		mask = pygame.mask.from_surface(self.image)
		self.image = mask.to_surface()
		self.image.set_colorkey("black")


	def update(self,dt):
		self.duration.update()
		if not self.duration.active: self.kill() 