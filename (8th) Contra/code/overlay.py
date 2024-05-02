import pygame
from pygame.math import Vector2
class Overlay:
	def __init__(self,player):
		self.player = player
		self.screen = pygame.display.get_surface()
		self.health_image = pygame.image.load("../graphics/health.png").convert_alpha()		

	def display(self):
		for i in range(self.player.health):
			x_pos = 4+ i * (self.health_image.get_width()+4)
			y_pos = 10
			pos = Vector2(x_pos,y_pos)
			self.screen.blit(self.health_image,pos)