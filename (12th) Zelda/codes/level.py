import pygame
# Files
from settings import *
from tile   import Tile
from player import Player
from enemy  import Enemy
from weapon import Weapon
from ui     import UI
from magic  import MagicPlayer
from particle import ParticleEffect,AnimationPlayer
from upgrade  import Upgrade
# Methods
from pygame.math import Vector2
from csv import reader
from os import walk
from random import choice,randint

class AllSprite(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.offset = Vector2(0,0)
		# BG
		self.bg = pygame.image.load("../graphics/tilemap/ground.png").convert()
		self.bg_rect = self.bg.get_rect(topleft=(0,0))

	def customize_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		bg_offset_pos = self.bg_rect.topleft - self.offset
		self.screen.blit(self.bg,bg_offset_pos)
		for sprite in sorted(self.sprites(),key = lambda sprite:sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image,offset_pos)

class Level:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.game_paused = False
		# Groups
		self.all_sprites = AllSprite()
		self.obstacle_sprites   = pygame.sprite.Group()
		self.attack_sprites     = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		# Setup
		self.create_map()
		self.current_attack = None
		# User interface
		self.ui = UI()
		self.upgrade = Upgrade(self.player)
		# Particle effect
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

	def import_csv_layout(self,path):
		terrain_map = []
		with open(path) as level_map:
			layout = reader(level_map,delimiter=",")
			for row in layout:
				terrain_map.append(row)
			return terrain_map

	def import_folder(self,path):
		image_list = []
		for _,_,images in walk(path):
			for image in images:
				full_path = path + "/" + image
				image = pygame.image.load(full_path).convert_alpha()
				image_list.append(image)
		return image_list

	def create_map(self):
		self.player = Player(
						self.all_sprites,
						(2000,1430),
						self.obstacle_sprites,
						self.create_attack,
						self.destroy_attack,
						self.create_magic
		)
		layouts = {
			"boundary": self.import_csv_layout("../map/map_FloorBlocks.csv"),
			"grass"   : self.import_csv_layout("../map/map_Grass.csv"),
			"object"  : self.import_csv_layout("../map/map_Objects.csv"),
			"entities": self.import_csv_layout("../map/map_Entities.csv")
		}
		graphics = {
			"grass" : self.import_folder("../graphics/grass"),
			"object": self.import_folder("../graphics/objects")
		}
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index,col in enumerate(row):
					if col != "-1":
						pos_x = col_index * TILESIZE
						pos_y = row_index * TILESIZE
						pos = (pos_x,pos_y)
						if style == "boundary":
							Tile([self.obstacle_sprites],pos,"invisible")
						if style == "grass":
							random_image = choice(graphics[style])
							Tile(
								[self.all_sprites,self.obstacle_sprites,self.attackable_sprites],
								pos,
								style,
								random_image
							)
						if style == "object":
							image = graphics[style][int(col)]
							Tile([self.all_sprites,self.obstacle_sprites],pos,style,image)
						if style == "entities":
							match col:
								case "390": monster_name = "bamboo"
								case "391": monster_name = "spirit"
								case "392": monster_name = "raccoon"
								case "393": monster_name = "squid"
							Enemy(
								[self.all_sprites,self.attackable_sprites],
								monster_name,
								pos,
								self.obstacle_sprites,
								self.player,
								self.damage_player,
								self.start_death_particles,
								self.add_player_exp
							)

	def create_attack(self):
		self.current_attack = Weapon([self.all_sprites,self.attack_sprites],self.player)

	def destroy_attack(self):
		if self.current_attack: self.current_attack.kill()
		self.current_attack = None

	def create_magic(self,style,strength,cost):
		match style:
			case "heal":
				self.magic_player.heal([self.all_sprites],self.player,strength,cost)
			case "flame":
				self.magic_player.flame([self.all_sprites,self.attack_sprites],self.player,cost)

	def player_attack(self):
		for attack_sprite in self.attack_sprites.sprites():
			collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
			for sprite in collision_sprites:
				if sprite.sprite_type == "grass":
					pos = sprite.rect.center
					offset = Vector2(0,75)
					for leaf in range(randint(3,6)):
						self.animation_player.create_grass_particles([self.all_sprites],pos-offset)
					sprite.kill()
				elif sprite.sprite_type == "enemy":
					sprite.damage(self.player,attack_sprite.sprite_type)

	def damage_player(self,amount,attack_type):
		if self.player.is_vulnerable:
			self.player.health -= amount
			self.player.is_vulnerable = False
			self.player.hit_time = pygame.time.get_ticks()
			self.animation_player.create_particles([self.all_sprites],self.player.rect.center,attack_type)

	def start_death_particles(self,pos,particle_type):
		self.animation_player.create_particles([self.all_sprites],pos,particle_type)

	def add_player_exp(self,amount):
		self.player.exp += amount

	def upgrade_menu(self):
		self.game_paused = not self.game_paused

	def run(self,dt):
		# Draw
		self.all_sprites.customize_draw(self.player)
		self.ui.display(self.player)
		if self.game_paused:
			self.upgrade.update()
		else:
			# Update
			self.all_sprites.update(dt)
			self.player_attack()