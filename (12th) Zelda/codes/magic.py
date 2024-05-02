import pygame
from settings import *
from pygame.math import Vector2
from random import randint

class MagicPlayer:
	def __init__(self,animation_player):
		self.animation_player = animation_player
		self.sounds = {
			"heal" : pygame.mixer.Sound("../musics/heal.ogg"),
			"flame": pygame.mixer.Sound("../musics/fire.ogg")
		}

	def heal(self,groups,player,strength,cost):
		if player.energy >= cost:
			self.sounds["heal"].play()
			player.health += strength
			player.energy -= cost
			if player.health >= player.stats["health"]:
				player.health = player.stats["health"]
			self.animation_player.create_particles(groups,player.rect.center,"aura")
			self.animation_player.create_particles(groups,player.rect.center,"heal")

	def flame(self,groups,player,cost):
		if player.energy >= cost:
			self.sounds["flame"].play()
			player.energy -= cost
			match player.status.split("_")[0]:
				case "right": direction = Vector2(1,0)
				case "left" : direction = Vector2(-1,0)
				case "up"   : direction = Vector2(0,-1)
				case "down" : direction = Vector2(0,1)
			for i in range(1,6):
				# Horizontal
				if direction.x:
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x + randint(-TILESIZE//3,TILESIZE//3)
					y = player.rect.centery + randint(-TILESIZE//3,TILESIZE//3)
					pos = (x,y)
					self.animation_player.create_particles(groups,pos,"flame")
				# Vertical
				else:
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx + randint(-TILESIZE//3,TILESIZE//3)
					y = player.rect.centery + offset_y + randint(-TILESIZE//3,TILESIZE//3)
					pos = (x,y)
					self.animation_player.create_particles(groups,pos,"flame")