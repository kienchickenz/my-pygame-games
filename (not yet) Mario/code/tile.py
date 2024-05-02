import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,groups,pos,size):
		super().__init__(groups)
		self.image = pygame.Surface((size,size))
		self.image.fill("grey")
		self.rect  = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()