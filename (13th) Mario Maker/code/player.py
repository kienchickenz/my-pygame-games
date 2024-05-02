import pygame
from pygame.math import Vector2

from settings import *
from sprites  import Generic
from timer    import Timer

class Player(Generic):
	def __init__(self,groups,pos,images,collision_sprites,jump_sound):
		# Animation
		self.animation = images
		self.status = "idle"
		self.orientation = "right"
		self.image_index = 0
		image = self.animation[f"{self.status}_{self.orientation}"][self.image_index]
		super().__init__(groups,pos,image)
		self.mask = pygame.mask.from_surface(self.image)
		# Movement
		self.direction = Vector2()
		self.pos = Vector2(self.rect.center)
		self.speed = 260
		self.gravity = 4
		self.jump_gravity = 2
		self.on_floor = False
		# Collision
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(-50,0)
		# Damage
		self.invul_timer = Timer(200)
		# Music
		self.jump_sound = jump_sound
		self.jump_sound.set_volume(0.2)

	def get_status(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 1:
			self.status = "fall"
		else:
			self.status = "run" if self.direction.x != 0 else "idle"

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.orientation = "right"
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.orientation = "left"
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_floor:
			self.direction.y = -self.jump_gravity
			self.jump_sound.play()

	def move(self,dt):
		# Horizontal movement
		self.pos.x += self.direction.x*self.speed*dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision("horizontal")
		# Vertical movement
		self.pos.y += self.direction.y*self.speed*dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision("vertical")

	def apply_gravity(self,dt):
		self.direction.y += self.gravity * dt
		self.rect.y += self.direction.y

	def collision(self,direction):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.hitbox):
				if direction == "horizontal":
					self.hitbox.right = sprite.rect.left if self.direction.x > 0 else self.hitbox.right
					self.hitbox.left = sprite.rect.right if self.direction.x < 0 else self.hitbox.left
					self.rect.centerx,self.pos.x = self.hitbox.centerx,self.hitbox.centerx
				elif direction == "vertical":
					self.hitbox.bottom = sprite.rect.top if self.direction.y > 0 else self.hitbox.bottom
					self.hitbox.top = sprite.rect.bottom if self.direction.y < 0 else self.hitbox.top
					self.rect.centery,self.pos.y = self.hitbox.centery,self.hitbox.centery
					self.direction.y = 0

	def check_on_floor(self):
		floor_rect = pygame.Rect((self.hitbox.bottomleft),(self.hitbox.width,2))
		floor_sprites = [sprite for sprite in self.collision_sprites 
							if sprite.rect.colliderect(floor_rect)]
		self.on_floor = True if floor_sprites else False

	def animate(self,dt):
		current_animation = self.animation[f"{self.status}_{self.orientation}"]
		self.image_index += ANIMATION_SPEED * dt
		if self.image_index >= len(current_animation): self.image_index = 0
		self.image = current_animation[int(self.image_index)]
		self.mask = pygame.mask.from_surface(self.image)
		if self.invul_timer.active:
			surf = self.mask.to_surface()
			surf.set_colorkey("black")
			self.image = surf

	def damage(self):
		if not self.invul_timer.active:
			self.invul_timer.activate()
			self.direction.y -= 1.5

	def update(self,dt):
		self.input()
		self.apply_gravity(dt)
		self.move(dt)
		self.check_on_floor()
		self.invul_timer.update()

		self.get_status()
		self.animate(dt)