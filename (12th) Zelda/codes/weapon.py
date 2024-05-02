import pygame
from settings import *
from pygame.math import Vector2

class Weapon(pygame.sprite.Sprite):
	def __init__(self,groups,player):
		super().__init__(groups)
		self.sprite_type = "weapon"
		direction = player.status.split("_")[0]
		path = f"../graphics/weapons/{player.weapon}/{direction}.png"
		self.image = pygame.image.load(path).convert_alpha()
		match direction:
			case "right":
				offset = Vector2(0,16)
				self.rect = self.image.get_rect(midleft = player.rect.midright + offset)
			case "left":
				offset = Vector2(0,16)
				self.rect = self.image.get_rect(midright = player.rect.midleft + offset)
			case "up":
				offset = Vector2(-10,0)
				self.rect = self.image.get_rect(midbottom = player.rect.midtop + offset)
			case "down":
				offset = Vector2(-10,0)
				self.rect = self.image.get_rect(midtop = player.rect.midbottom + offset)