import pygame
from settings   import *
from player     import Player
from overlay    import Overlay
from sprites    import Generic,Water,WildFlower,Tree,Interaction,Particle
from supports   import *
from transition import Transition
from soil       import SoilLayer
from sky        import Rain,Sky
from menu       import Menu

from pygame.image import load
from pygame.math  import Vector2
from random       import randint
from pytmx.util_pygame import load_pygame

class Level:
	def __init__(self):
		# Defaults
		self.screen = pygame.display.get_surface()
		# Groups
		self.all_sprites = AllSprites()
		self.collision_sprites   = pygame.sprite.Group()
		self.tree_sprites        = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()
		# Setup
		self.soil_layer = SoilLayer(self.all_sprites,self.collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset,self.player)
		# Sky
		self.sky = Sky()
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		# Shop
		self.menu_active = False
		self.menu = Menu(self.player,self.toggle_menu)
		# Sound
		self.success_sound = pygame.mixer.Sound("../music/success.ogg")
		self.success_sound.set_volume(0.3)
		self.music = pygame.mixer.Sound("../music/music.ogg")
		self.music.set_volume(0.2)
		self.music.play(loops=-1)

	def setup(self):
		tmx_data = load_pygame("../data/map.tmx")
		# House
		for layer in ["HouseFloor","HouseFurnitureBottom"]:
			for x,y,image in tmx_data.get_layer_by_name(layer).tiles():
				Generic(self.all_sprites,(x*TILE_SIZE,y*TILE_SIZE),image,LAYERS["house bottom"])
		for layer in ["HouseWalls","HouseFurnitureTop"]:
			for x,y,image in tmx_data.get_layer_by_name(layer).tiles():
				Generic(self.all_sprites,(x*TILE_SIZE,y*TILE_SIZE),image)
		# Fence
		for x,y,image in tmx_data.get_layer_by_name("Fence").tiles():
			Generic([self.all_sprites,self.collision_sprites],(x*TILE_SIZE,y*TILE_SIZE),image)
		# Water
		water_images = import_folder("../graphics/water")
		for x,y,image in tmx_data.get_layer_by_name("Water").tiles():
			Water(self.all_sprites,(x*TILE_SIZE,y*TILE_SIZE),water_images)
		# Tree
		for obj in tmx_data.get_layer_by_name("Trees"):
			Tree(
				[self.all_sprites,self.collision_sprites,self.tree_sprites],
				(obj.x,obj.y),
				obj.image,
				obj.name,
				self.add_inventory
				)
		# Wildflower
		for obj in tmx_data.get_layer_by_name("Decoration"):
			WildFlower([self.all_sprites,self.collision_sprites],(obj.x,obj.y),obj.image)
		# Ground
		Generic(self.all_sprites,(0,0),load("../graphics/world/ground.png").convert_alpha(),LAYERS["ground"])
		# Border
		for x,y,image in tmx_data.get_layer_by_name("Collision").tiles():
			Generic([self.collision_sprites],(x*TILE_SIZE,y*TILE_SIZE),pygame.Surface((TILE_SIZE,TILE_SIZE)))
		# Player
		for obj in tmx_data.get_layer_by_name("Player"):
			if obj.name == "Start":
				pos = (obj.x,obj.y)
				self.player = Player(
								self.all_sprites,
								pos,
								self.collision_sprites,
								self.tree_sprites,
								self.interaction_sprites,
								self.soil_layer,
								self.toggle_menu
								)
			if obj.name == "Bed":
				Interaction(self.interaction_sprites,(obj.width,obj.height),(obj.x,obj.y),obj.name)
			if obj.name == "Trader":
				Interaction(self.interaction_sprites,(obj.width,obj.height),(obj.x,obj.y),obj.name)

	def add_inventory(self,item):
		self.player.item_inventory[item] += 1
		self.success_sound.play()

	def toggle_menu(self):
		self.menu_active = not self.menu_active

	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites:
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.add_inventory(plant.plant_type)
					plant.kill()
					Particle(self.all_sprites,plant.rect.topleft,plant.image,LAYERS["main"])
					col_index = plant.rect.centerx // TILE_SIZE
					row_index = plant.rect.centery // TILE_SIZE
					self.soil_layer.grid[row_index][col_index].remove("P")

	def reset(self):
		# Plants
		self.soil_layer.update_plants()
		# Apples
		for tree in self.tree_sprites:
			if tree.alive:
				for apple in tree.apple_sprites:
					apple.kill()
				tree.create_fruit()
				tree.health = 5
		# Soil
		self.soil_layer.remove_water()
		self.raining = randint(0,10) > 7
		# Rain
		self.soil_layer.raining = self.raining
		# Sky
		self.sky.start_color = [255,255,255]

	def run(self,dt):
		# Draw
		self.all_sprites.custom_draw(self.player)
		self.overlay.display()
		# Update
		if self.menu_active:
			self.menu.update()
		else:
			self.all_sprites.update(dt)
			self.plant_collision()
			# Rain
			if self.raining:
				self.rain.update()
				self.soil_layer.water_all()
		# Daytime
		self.sky.display(dt)
		if self.player.sleep:
			self.transition.play()

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.offset = Vector2()

	def custom_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		for layer in LAYERS.values():
			for sprite in sorted(self,key=lambda sprite:sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.screen.blit(sprite.image,offset_rect)
					# Testing
					# if sprite == player:
					# 	pygame.draw.rect(self.screen,"red",offset_rect,5)
					# 	hitbox_rect = player.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.screen,"green",hitbox_rect,5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split("_")[0]]
					# 	pygame.draw.circle(self.screen,"blue",target_pos,5)
