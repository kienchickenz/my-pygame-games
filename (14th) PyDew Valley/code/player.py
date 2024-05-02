import pygame
from settings import *
from timer    import Timer

from pygame.math import Vector2
from os          import walk

class Player(pygame.sprite.Sprite):
	def __init__(self,groups,pos,collision_sprites,tree_sprites,interaction_sprites,soil_layer,toggle_menu):
		super().__init__(groups)
		# Animation
		self.animation = self.imports("../graphics/player/")
		self.status = "down_idle"
		self.image_index = 0
		self.animation_speed = 4
		# Image
		self.image = self.animation[self.status][self.image_index]
		self.rect  = self.image.get_rect(center=pos)
		self.z = LAYERS["main"]
		# Movement
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 180
		# Collision
		self.hitbox = self.rect.copy().inflate(-126,-70)
		self.collision_sprites = collision_sprites
		# Timers
		self.timers = {
			"tool_use":Timer(500,self.use_tool),
			"tool_switch":Timer(300),
			"seed_use":Timer(500,self.use_seed),
			"seed_switch":Timer(300)
		}
		# Tools
		self.tools = ["hoe","axe","water"]
		self.tool_index = 0
		self.selected_tool = self.tools[self.tool_index]
		# Seeds
		self.seeds = ["corn","tomato"]
		self.seed_index = 0
		self.selected_seed = self.seeds[self.seed_index]
		# Inventory
		self.item_inventory = {
			"wood"  :0,
			"apple" :0,
			"corn"  :0,
			"tomato":0
		}
		self.seed_inventory = {
			"corn"  :5,
			"tomato":5
		}
		self.money = 0
		# Interactions
		self.tree_sprites = tree_sprites
		self.target_pos = Vector2()
		self.interaction_sprites = interaction_sprites
		self.sleep = False
		self.soil_layer = soil_layer
		# Shop
		self.toggle_menu = toggle_menu
		# Sound
		self.watering_sound = pygame.mixer.Sound("../music/water.ogg")
		self.watering_sound.set_volume(0.2)

	def imports(self,path):
		animation = {}
		for index,folder in enumerate(walk(path)):
			if index == 0:
				for folder_name in folder[1]:
					animation[folder_name] = []
			else:
				for file_name in folder[2]:
					full_path = f"{folder[0]}/{file_name}"
					image = pygame.image.load(full_path).convert_alpha()
					key = folder[0].split("/")[-1]
					animation[key].append(image)
		return animation

	def input(self):
		keys = pygame.key.get_pressed()
		if not self.timers["tool_use"].active and not self.timers["seed_use"].active and not self.sleep:
			# Direction
			if keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = "left"
			elif keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = "right"
			else:
				self.direction.x = 0
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = "up"
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = "down"
			else:
				self.direction.y = 0
			# Use tool
			if keys[pygame.K_SPACE]:
				self.timers["tool_use"].activate()
				self.direction = Vector2()
				self.image_index = 0
			# Change tool
			if keys[pygame.K_a] and not self.timers["tool_switch"].active:
				self.timers["tool_switch"].activate()
				self.tool_index += 1
				if self.tool_index >= len(self.tools): self.tool_index = 0
				self.selected_tool = self.tools[self.tool_index]
			# Seed use
			if keys[pygame.K_LCTRL]:
				self.timers["seed_use"].activate()
				self.direction = Vector2()
			# Change seed
			if keys[pygame.K_d] and not self.timers["seed_switch"].active:
				self.timers["seed_switch"].activate()
				self.seed_index += 1
				if self.seed_index >= len(self.seeds): self.seed_index = 0
				self.selected_seed = self.seeds[self.seed_index]
			# Interaction
			if keys[pygame.K_RETURN]:
				collided_interaction_sprites = pygame.sprite.spritecollide(self,self.interaction_sprites,False)
				if collided_interaction_sprites:
					match collided_interaction_sprites[0].name:
						case "Trader": 
							self.toggle_menu()
						case "Bed":
							self.status = "left_idle"
							self.sleep = True
							self.direction = Vector2()			

	def get_status(self):
		# Idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split("_")[0] + "_idle"
		# Tool
		if self.timers["tool_use"].active:
			self.status = self.status.split("_")[0] + f"_{self.selected_tool}"

	def collision(self,direction):
		for sprite in self.collision_sprites:
			if hasattr(sprite,"hitbox"):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == "horizontal":
						if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right	
						self.rect.centerx,self.pos.x = self.hitbox.centerx,self.hitbox.centerx
					elif direction == "vertical":
						if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom
						if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
						self.rect.centery,self.pos.y = self.hitbox.centery,self.hitbox.centery

	def move(self,dt):
		if self.direction.magnitude() != 0: self.direction = self.direction.normalize()
		# Horizontal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.centerx,self.hitbox.centerx = round(self.pos.x),round(self.pos.x)
		self.collision("horizontal")
		# Vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.centery,self.hitbox.centery = round(self.pos.y),round(self.pos.y)
		self.collision("vertical")

	def animate(self,dt):
		current_animation = self.animation[self.status]
		self.image_index += self.animation_speed * dt
		if self.image_index >= len(current_animation): self.image_index = 0
		self.image = current_animation[int(self.image_index)]

	def get_target_pos(self):
		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split("_")[0]]

	def use_tool(self):
		match self.selected_tool:
			case "axe"  : 
				for tree in self.tree_sprites:
					if tree.rect.collidepoint(self.target_pos): tree.damage()
			case "hoe"  : 
				self.soil_layer.get_hit(self.target_pos)
			case "water": 
				self.soil_layer.water(self.target_pos)
				self.watering_sound.play()

	def use_seed(self):
		if self.seed_inventory[self.selected_seed] > 0:
			self.soil_layer.plant_seed(self.target_pos,self.selected_seed)
			self.seed_inventory[self.selected_seed] -= 1

	def update_timers(self):
		for timer in self.timers.values(): timer.update()

	def update(self,dt):
		self.input()
		self.get_status()
		self.update_timers()
		self.get_target_pos()

		self.move(dt)
		self.animate(dt)