import pygame
from settings import *
from entity   import Entity
from pygame.math import Vector2
from math import sin

class Player(Entity):
	def __init__(self,groups,pos,obstacle_sprites,create_attack,destroy_attack,create_magic):
		super().__init__(groups)
		# Animation setup
		self.import_images("../graphics/player")
		self.status = "down_idle"
		self.image_index = 0
		self.animation_speed = 8
		# Image setup
		self.image = self.animations[self.status][self.image_index]
		self.rect  = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET["player"])
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(0,0)
		self.speed_factor = 50
		# Collision
		self.obstacle_sprites = obstacle_sprites
		# Attack
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = 0
		self.create_attack = create_attack
		# Weapon
		self.weapon_index = 0
		self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
		self.destroy_attack = destroy_attack
		self.can_switch_weapon = True
		self.weapon_switch_cooldown = 200
		self.weapon_switch_time = 0
		# Magic
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(MAGIC_DATA.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_cooldown = 200
		self.magic_switch_time = 0
		# Stat
		self.stats = {"health":100,"energy":60,"attack":10,"magic":4,"speed":6}
		self.max_stats = {"health":300,"energy":140,"attack":20,"magic":10,"speed":10}
		self.upgrade_cost = {"health":100,"energy":100,"attack":100,"magic":100,"speed":100}
		self.health = self.stats["health"]
		self.energy = self.stats["energy"]
		self.speed  = self.stats["speed"]
		self.exp = 500
		# Health
		self.is_vulnerable = True
		self.hit_time = 0
		self.vulnerability_time = 500
		# Sound
		self.weapon_attack_sound = pygame.mixer.Sound("../musics/sword.ogg")
		self.weapon_attack_sound.set_volume(0.4)

	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			self.status = self.status.split("_")[0] + "_idle"
		if self.attacking:
			self.status = self.status.split("_")[0] + "_attack"

	def input(self):
		keys = pygame.key.get_pressed()
		if not self.attacking:
			# Move input
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
			# Attack input
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.direction = Vector2(0,0)
				self.create_attack()
				self.weapon_attack_sound.play()
			# Magic input
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.direction = Vector2(0,0)				
				self.do_magic()
			# Switch weapon
			if keys[pygame.K_a]:
				if self.can_switch_weapon: self.switch_weapon()
			# Switch magic
			if keys[pygame.K_d]:
				if self.can_switch_magic: self.switch_magic()

	def switch_magic(self):
		self.magic_index += 1
		if self.magic_index >= len(list(MAGIC_DATA.keys())):
			self.magic_index = 0
		self.magic = list(MAGIC_DATA.keys())[self.magic_index]
		self.can_switch_magic = False
		self.magic_switch_time = pygame.time.get_ticks()

	def do_magic(self):
		style = self.magic
		strength = MAGIC_DATA[style]["strength"] + self.stats["magic"]
		cost     = MAGIC_DATA[style]["cost"]
		self.create_magic(style,strength,cost)

	def switch_weapon(self):
		self.weapon_index += 1
		if self.weapon_index >= len(list(WEAPON_DATA.keys())):
			self.weapon_index = 0
		self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
		self.can_switch_weapon = False
		self.weapon_switch_time = pygame.time.get_ticks()

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			attack_cooldown = self.attack_cooldown + WEAPON_DATA[self.weapon]["cooldown"]
			if current_time - self.attack_time > attack_cooldown:
				self.attacking = False
				self.destroy_attack()
		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time > self.weapon_switch_cooldown:
				self.can_switch_weapon = True
		if not self.can_switch_magic:
			if current_time - self.magic_switch_time > self.magic_switch_cooldown:
				self.can_switch_magic = True
		if not self.is_vulnerable:
			if current_time - self.hit_time > self.vulnerability_time:
				self.is_vulnerable = True

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += self.animation_speed*dt
		if self.image_index >= len(current_animation): self.image_index = 0
		self.image = current_animation[int(self.image_index)]

	def get_full_weapon_damage(self):
		weapon_damage = self.stats["attack"] + WEAPON_DATA[self.weapon]["damage"]
		return weapon_damage

	def get_full_magic_damage(self):
		magic_damage = self.stats["magic"] + MAGIC_DATA[self.magic]["strength"]
		return magic_damage

	def blink(self):
		if not self.is_vulnerable:
			wave_value = sin(pygame.time.get_ticks())
			if wave_value > 0:
				mask = pygame.mask.from_surface(self.image)
				white_surface = mask.to_surface()
				white_surface.set_colorkey("black")
				self.image = white_surface

	def energy_recovery(self):
		if self.energy < self.stats["energy"]:
			self.energy += 0.005 * self.stats["magic"]
		else:
			self.energy = self.stats["energy"]

	def update(self,dt):
		self.input()
		self.move(dt,self.stats["speed"]*self.speed_factor)

		self.get_status()
		self.animate(dt)

		self.energy_recovery()
		self.cooldowns()

		self.blink()