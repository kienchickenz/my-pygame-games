import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,groups,pos,sprite_type,image=pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = image
		y_offset = HITBOX_OFFSET[sprite_type]
		if sprite_type == "object":
			offset_pos = (pos[0],pos[1]-64)
			self.rect = self.image.get_rect(topleft=offset_pos)
		else:
			self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,y_offset)