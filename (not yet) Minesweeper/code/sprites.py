import pygame
from settings import *
from pygame.math import Vector2

class Tile(pygame.sprite.Sprite):
	def __init__(self,groups,pos,image,type,is_revealed=False,is_flagged=False):
		super().__init__(groups)
		self.image = image
		self.rect  = self.image.get_rect(topleft=(Vector2(pos)*TILESIZE))

class Board:
	def __init__(self,all_sprites,images):
		self.screen = pygame.display.get_surface()
		self.all_sprites = all_sprites
		self.images = images
		self.tiles = [[Tile(self.all_sprites,(row,col),self.images["unknown"],TILE_STATUS[0]) 
						for col in range(COLS)] for row in range(ROWS)]