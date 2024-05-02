import pygame
from settings import *

from pygame.image import load

class Overlay:
	def __init__(self,player):
		self.screen = pygame.display.get_surface()
		self.player = player
		# Images
		overlay_path = "../graphics/overlay"
		self.tool_images = {tool:load(f"{overlay_path}/{tool}.png").convert_alpha() for tool in player.tools}
		self.seed_images = {seed:load(f"{overlay_path}/{seed}.png").convert_alpha() for seed in player.seeds}
	
	def display(self):
		# Tool
		tool_image = self.tool_images[self.player.selected_tool]
		tool_rect  = tool_image.get_rect(midbottom=OVERLAY_POSITIONS["tool"]) 
		self.screen.blit(tool_image,tool_rect)
		# Seed
		seed_image = self.seed_images[self.player.selected_seed]
		seed_rect  = seed_image.get_rect(midbottom=OVERLAY_POSITIONS["seed"]) 
		self.screen.blit(seed_image,seed_rect)