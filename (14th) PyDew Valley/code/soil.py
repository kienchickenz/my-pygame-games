import pygame
from settings import *
from supports import *
from sprites  import Generic

from pytmx.util_pygame import load_pygame
from random      import choice
from pygame.math import Vector2

class SoilLayer:
	def __init__(self,all_sprites,collision_sprites):
		# Groups
		self.all_sprites       = all_sprites
		self.collision_sprites = collision_sprites
		self.soil_sprites  = pygame.sprite.Group()
		self.water_sprites = pygame.sprite.Group()
		self.plant_sprites = pygame.sprite.Group()
		# Images
		self.soil_images  = import_folder_dict("../graphics/soil/")
		self.water_images = import_folder("../graphics/soil_water/")
		# Setup
		self.grid = []
		self.create_soil_grid()
		self.hit_rects = []
		self.create_hit_rects()
		# Sound
		self.hoe_sound = pygame.mixer.Sound("../music/hoe.ogg")
		self.hoe_sound.set_volume(0.1)
		self.plant_sound = pygame.mixer.Sound("../music/plant.ogg")
		self.plant_sound.set_volume(0.2)

	def create_soil_grid(self):
		ground = pygame.image.load("../graphics/world/ground.png")
		horizontal_tiles,vertical_tiles = ground.get_width()//TILE_SIZE,ground.get_height()//TILE_SIZE
		self.grid = [ [[] for col in range(horizontal_tiles)] for row in range(vertical_tiles)]
		for col,row,_ in load_pygame("../data/map.tmx").get_layer_by_name("Farmable").tiles():
			self.grid[row][col].append("F")

	def create_hit_rects(self):
		self.hit_rects = []
		for row_index,row in enumerate(self.grid):
			for col_index,cell in enumerate(row):
				if "F" in cell:
					x = col_index * TILE_SIZE
					y = row_index * TILE_SIZE
					rect = pygame.Rect((x,y),(TILE_SIZE,TILE_SIZE))
					self.hit_rects.append(rect)

	def get_hit(self,point):
		for rect in self.hit_rects:
			if rect.collidepoint(point):
				self.hoe_sound.play()
				col_index = rect.x // TILE_SIZE
				row_index = rect.y // TILE_SIZE
				if 'F' in self.grid[row_index][col_index]:
					self.grid[row_index][col_index].append("X")
					self.create_soil_tiles()

	def check_soil_type(self,row_index,col_index):
		t = "X" in self.grid[row_index - 1][col_index]
		b = "X" in self.grid[row_index + 1][col_index]
		l = "X" in self.grid[row_index][col_index - 1]
		r = "X" in self.grid[row_index][col_index + 1]
		soil_type = "o"
		# All sides
		if all([t,b,l,r]): soil_type = "x"
		# Horizontal sides
		if l and not any([t,b,r]): soil_type = "r"
		if r and not any([t,b,l]): soil_type = "l"
		if all([l,r]) and not any([t,b]): soil_type = "lr"
		# Vertical sides
		if t and not any([l,r,b]): soil_type = "b"
		if b and not any([t,l,r]): soil_type = "t"
		if all([t,b]) and not any([l,r]): soil_type = "tb"
		# Corners
		if all([b,l]) and not any([t,r]): soil_type = "tr"
		if all([b,r]) and not any([t,l]): soil_type = "tl"
		if all([t,l]) and not any([b,r]): soil_type = "br"
		if all([t,r]) and not any([b,l]): soil_type = "bl"
		# T-Shapes
		if all([t,b,r]) and not l: soil_type = "tbr"
		if all([t,b,l]) and not r: soil_type = "tbl"
		if all([l,r,b]) and not t: soil_type = "lrt"
		if all([l,r,t]) and not b: soil_type = "lrb"
		return soil_type

	def create_soil_tiles(self):
		self.soil_sprites.empty()
		for row_index,row in enumerate(self.grid):
			for col_index,cell in enumerate(row):
				if "X" in cell:
					soil_type = self.check_soil_type(row_index,col_index)
					pos = (col_index * TILE_SIZE,row_index * TILE_SIZE)
					SoilTile([self.all_sprites,self.soil_sprites],pos,self.soil_images[soil_type])

	def water(self,target_pos):
		for soil_sprite in self.soil_sprites:
			if soil_sprite.rect.collidepoint(target_pos):
				col_index = soil_sprite.rect.x // TILE_SIZE
				row_index = soil_sprite.rect.y // TILE_SIZE
				self.grid[row_index][col_index].append("W")
				# Water
				water_pos = soil_sprite.rect.topleft
				water_image = choice(self.water_images)
				WaterTile([self.all_sprites,self.water_sprites],water_pos,water_image)

	def water_all(self):
		for row_index,row in enumerate(self.grid):
			for col_index,cell in enumerate(row):
				if "X" in cell and "W" not in cell:
					cell.append("W")
					water_pos = (col_index * TILE_SIZE,row_index * TILE_SIZE)
					water_image = choice(self.water_images)
					WaterTile([self.all_sprites,self.water_sprites],water_pos,water_image)

	def remove_water(self):
		for sprite in self.water_sprites: sprite.kill()
		for row in self.grid:
			for cell in row:
				if "W" in cell: cell.remove("W")

	def check_watered(self,pos):
		col_index = pos[0] // TILE_SIZE
		row_index = pos[1] // TILE_SIZE
		cell = self.grid[row_index][col_index]
		is_watered = "W" in cell
		return is_watered

	def plant_seed(self,target_pos,seed):
		for soil_sprite in self.soil_sprites:
			if soil_sprite.rect.collidepoint(target_pos):
				row_index = soil_sprite.rect.y // TILE_SIZE
				col_index = soil_sprite.rect.x // TILE_SIZE
				if "P" not in self.grid[row_index][col_index]:
					self.plant_sound.play()
					self.grid[row_index][col_index].append("P")
					Plant([self.all_sprites,self.plant_sprites,self.collision_sprites],seed,soil_sprite,self.check_watered)

	def update_plants(self):
		for plant in self.plant_sprites:
			plant.grow()

class SoilTile(Generic):
	def __init__(self,groups,pos,image):
		super().__init__(groups,pos,image,LAYERS["soil"])

class WaterTile(Generic):
	def __init__(self,groups,pos,image):
		super().__init__(groups,pos,image,LAYERS["soil water"])

class Plant(pygame.sprite.Sprite):
	def __init__(self,groups,plant_type,soil,check_watered):
		super().__init__(groups)
		# Setup
		self.plant_type = plant_type
		self.images = import_folder(f"../graphics/fruit/{plant_type}")
		self.soil = soil
		self.check_watered = check_watered
		# Growing
		self.age = 0
		self.max_age = len(self.images) - 1
		self.grow_speed = GROW_SPEED[plant_type]
		self.harvestable = False
		# Images
		self.image = self.images[self.age]
		self.y_offset = Vector2(0,-16) if plant_type == "corn" else Vector2(0,-8)
		self.rect  = self.image.get_rect(midbottom=soil.rect.midbottom + self.y_offset)
		self.z = LAYERS["ground plant"]

	def grow(self):
		if self.check_watered(self.rect.center):
			self.age += self.grow_speed
			if int(self.age) > 0: 
				self.z = LAYERS["main"]
				self.hitbox = self.rect.copy().inflate(-26,-self.rect.height * 0.5)
			if self.age >= self.max_age: 
				self.age = self.max_age
				self.harvestable = True
			self.image = self.images[int(self.age)]
			self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + self.y_offset)