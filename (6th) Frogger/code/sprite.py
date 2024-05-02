<<<<<<< HEAD
import pygame

class SimpleSprite(pygame.sprite.Sprite):
	def __init__(self,image,pos,groups):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height/2)

class LongSprite(pygame.sprite.Sprite):
	def __init__(self,image,pos,groups):
		super().__init__(groups)
		self.image  = image
		self.rect   = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-self.rect.width*0.8,-self.rect.height/2)
=======
import pygame

class SimpleSprite(pygame.sprite.Sprite):
	def __init__(self,image,pos,groups):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height/2)

class LongSprite(pygame.sprite.Sprite):
	def __init__(self,image,pos,groups):
		super().__init__(groups)
		self.image  = image
		self.rect   = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-self.rect.width*0.8,-self.rect.height/2)
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
		self.hitbox.bottom = self.rect.bottom - 10