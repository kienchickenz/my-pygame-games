import pygame
from settings import *
from tile   import Tile
from player import Player
from pygame.math import Vector2

class AllSprite(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.offset = Vector2(0,0)

	def customize_draw(self,player):
		constraint_left = WINDOW_WIDTH/4
		constraint_right = WINDOW_WIDTH - WINDOW_WIDTH/4
		if player.rect.x < constraint_left:
			self.offset.x = player.rect.x - constraint_left
			for sprite in self.sprites():
				offset_pos = sprite.rect.topleft - self.offset
				self.screen.blit(sprite.image,offset_pos)
		elif player.rect.x > constraint_right:
			self.offset.x = player.rect.x - constraint_right
			for sprite in self.sprites():
				offset_pos = sprite.rect.topleft - self.offset
				self.screen.blit(sprite.image,offset_pos)
		else:
			for sprite in self.sprites():
				self.screen.blit(sprite.image,sprite.rect)

class Level:
	def __init__(self,level_data):
		self.screen = pygame.display.get_surface()
		# Groups
		self.all_sprites = AllSprite()
		self.collision_sprites = pygame.sprite.Group()
		# Setup
		self.create_map(level_data)

	def create_map(self,layout):
		for row_index,row in enumerate(layout):
			for col_index,col in enumerate(row):
				pos_x = col_index * TILESIZE
				pos_y = row_index * TILESIZE
				pos = (pos_x,pos_y)
				match col:
					case "X":
						Tile([self.all_sprites,self.collision_sprites],pos,TILESIZE)
					case "P":
						self.player = Player([self.all_sprites],pos,self.collision_sprites)

	def run(self,dt):
		self.all_sprites.customize_draw(self.player)
		self.all_sprites.update(dt)