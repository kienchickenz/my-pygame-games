import pygame
from settings import *
from entity   import Entity
from pygame.math import Vector2
from math import sin

class Enemy(Entity):
	def __init__(self,groups,monster_name,pos,obstacle_sprites,player,damage_player,start_death_particles,add_player_exp):
		super().__init__(groups)
		self.sprite_type = "enemy"
		# Animation setup
		self.import_images(f"../graphics/monsters/{monster_name}")
		self.status = "idle"
		self.image_index = 0
		self.animation_speed = 8
		# Image
		self.image = self.animations[self.status][self.image_index]
		self.rect  = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,-10)
		# Move
		self.pos = Vector2(self.rect.topleft)
		self.direction = Vector2(0,0)
		self.speed_factor = 50
		# Collision
		self.obstacle_sprites = obstacle_sprites
		# Stats
		self.monster_name = monster_name
		monster_info = MONSTER_DATA[monster_name]
		self.health = monster_info["health"]
		self.exp    = monster_info["exp"]
		self.speed  = monster_info["speed"]
		self.attack_damage = monster_info["damage"]
		self.resistance = monster_info["resistance"]
		self.attack_radius = monster_info["attack_radius"]
		self.notice_radius = monster_info["notice_radius"]
		self.attack_type   = monster_info["attack_type"]
		# Attack
		self.player = player
		self.can_attack = True
		self.attack_time = 0
		self.attack_cooldown = 500
		self.damage_player = damage_player
		# Health
		self.is_vulnerable = True
		self.hit_time = 0
		self.vulnerability_time = 300
		self.start_death_particles = start_death_particles
		self.add_player_exp = add_player_exp
		# Sound
		self.death_sound = pygame.mixer.Sound("../musics/death.ogg")
		self.death_sound.set_volume(0.6)
		self.hit_sound = pygame.mixer.Sound("../musics/hit.ogg")
		self.hit_sound.set_volume(0.6)
		self.attack_sound = pygame.mixer.Sound(monster_info["attack_sound"])
		self.attack_sound.set_volume(0.3)

	def get_player_distance_direction(self,player):
		enemy_pos  = Vector2(self.rect.center)
		player_pos = Vector2(player.rect.center)
		distance  = (player_pos - enemy_pos).magnitude()
		if distance > 0:
			direction = (player_pos - enemy_pos).normalize()
		else:
			direction = Vector2(0,0)
		return (distance,direction)

	def move(self,dt,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		# Horizontal movement
		self.pos.x += self.direction.x*speed*dt
		self.rect.x = round(self.pos.x)
		self.hitbox.centerx = self.rect.centerx
		self.collision("horizontal")
		# Vertical movement
		self.pos.y += self.direction.y*speed*dt
		self.rect.y = round(self.pos.y)
		self.hitbox.centery = self.rect.centery
		self.collision("vertical")

	def get_status(self,player):
		distance = self.get_player_distance_direction(player)[0]
		if distance <= self.attack_radius and self.can_attack:
			if self.status != "attack":
				self.image_index = 0
			self.status = "attack"
		elif distance <= self.notice_radius:
			self.status = "move"
		else:
			self.status = "idle"

	def actions(self,player):
		if self.status == "attack":
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_time = pygame.time.get_ticks()
			self.attack_sound.play(6)
		elif self.status == "move":
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = Vector2(0,0)

	def animate(self,dt):
		current_animation = self.animations[self.status]
		self.image_index += self.animation_speed*dt
		if self.image_index >= len(current_animation): 
			self.image_index = 0
			if self.can_attack: self.can_attack = False
		self.image = current_animation[int(self.image_index)]

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True
		if not self.is_vulnerable:
			if current_time - self.hit_time >= self.vulnerability_time:
				self.is_vulnerable = True

	def damage(self,player,attack_type):
		if self.is_vulnerable: 
			self.direction = self.get_player_distance_direction(player)[1]
			self.is_vulnerable = False
			self.hit_time = pygame.time.get_ticks()
			self.hit_sound.play()
			if attack_type == "weapon":
				self.health -= player.get_full_weapon_damage()
			elif attack_type == "magic":
				self.health -= player.get_full_magic_damage()

	def hit_reaction(self):
		if not self.is_vulnerable:
			match self.player.status.split("_")[0]:
				case "right": self.direction = Vector2(1,0)
				case "left" : self.direction = Vector2(-1,0)
				case "down" : self.direction = Vector2(0,1)
				case "up"   : self.direction = Vector2(0,-1)

	def check_death(self):
		if self.health <= 0: 
			self.start_death_particles(self.rect.center,self.monster_name)	
			self.add_player_exp(self.exp)
			self.kill()
			self.death_sound.play()

	def blink(self):
		if not self.is_vulnerable:
			wave_value = sin(pygame.time.get_ticks())
			if wave_value > 0:
				mask = pygame.mask.from_surface(self.image)
				white_surface = mask.to_surface()
				white_surface.set_colorkey("black")
				self.image = white_surface

	def update(self,dt):
		self.get_status(self.player)
		self.actions(self.player)
		self.move(dt,self.speed*self.speed_factor)
		self.animate(dt)

		self.cooldowns()

		self.blink()
		self.hit_reaction()
		self.check_death()