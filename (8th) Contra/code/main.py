<<<<<<< HEAD
import pygame,sys
from settings import *
from tile     import Tile,CollisionTile,MovingPlatform
from player   import Player 
from enemy    import Enemy
from bullet   import Bullet,FireAnimation
from overlay  import Overlay
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2

class AllSprite(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.offset = Vector2(0,0)
		# SKY
		# Image
		self.fg_sky = pygame.image.load("../graphics/sky/fg_sky.png").convert_alpha()
		self.bg_sky = pygame.image.load("../graphics/sky/bg_sky.png").convert_alpha()
		tmx_map = load_pygame("../data/map.tmx")
		# Dimensions
		self.padding = WINDOW_WIDTH/2
		self.sky_width = self.bg_sky.get_width()
		map_width = tmx_map.tilewidth*tmx_map.width + 2*self.padding
		self.sky_num = int(map_width // self.sky_width)

	def customize_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		for x in range(self.sky_num):
			x_pos = -self.padding + (x*self.sky_width)
			bg_pos = Vector2(x_pos,800) - self.offset/2.5
			fg_pos = Vector2(x_pos,800) - self.offset/2
			self.screen.blit(self.bg_sky,bg_pos)
			self.screen.blit(self.fg_sky,fg_pos)
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.z):
			offset_rect = sprite.image.get_rect(center=sprite.rect.center)
			offset_rect.center -= self.offset
			self.screen.blit(sprite.image,offset_rect)

class Game:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My eighth python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		# Groups
		self.all_sprites = AllSprite()
		self.collision_sprites  = pygame.sprite.Group()
		self.platform_sprites   = pygame.sprite.Group()
		self.bullet_sprites     = pygame.sprite.Group()
		self.vulnerable_sprites = pygame.sprite.Group()
		self.setup()
		self.overlay = Overlay(self.player)
		# Image
		self.bullet_image = pygame.image.load("../graphics/bullet.png").convert_alpha()
		self.fire_images  = [
			pygame.image.load("../graphics/fire/0.png").convert_alpha(),
			pygame.image.load("../graphics/fire/1.png").convert_alpha()
			]
		# Music
		self.music =  pygame.mixer.Sound("../audio/music.ogg")
		self.music.play(loops=-1)

	def setup(self):
		tmx_map = load_pygame("../data/map.tmx")
		# Tiles
		for x,y,image in tmx_map.get_layer_by_name("Level").tiles():
			CollisionTile(
				pos=(tmx_map.tilewidth*x,tmx_map.tilewidth*y),
				image=image,
				groups=[self.all_sprites,self.collision_sprites]
				)
		for layer in ["BG","BG Detail","FG Detail Bottom","FG Detail Top"]:
			for x,y,image in tmx_map.get_layer_by_name(layer).tiles():
				Tile(
					pos=(tmx_map.tilewidth*x,tmx_map.tilewidth*y),
					image=image,
					groups=[self.all_sprites],
					z=LAYERS[layer]
					)
		# Objects
		for obj in tmx_map.get_layer_by_name("Entities"):
			match obj.name:
				case "Player":
					self.player = Player(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites,self.vulnerable_sprites],
						path="../graphics/player",
						collision_sprite=self.collision_sprites,
						create_bullet=self.create_bullet
						)
				case "Enemy":
					Enemy(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites,self.vulnerable_sprites],
						path="../graphics/enemy",
						create_bullet=self.create_bullet,
						player=self.player,
						collision_sprites=self.collision_sprites
						)
		self.platform_borders = []
		for obj in tmx_map.get_layer_by_name("Platforms"):
			match obj.name:
				case "Platform":
					MovingPlatform(
						pos=(obj.x,obj.y),
						image=obj.image,
						groups=[self.all_sprites,self.collision_sprites,self.platform_sprites]
						)
				case "Border": 
					border_rect = pygame.Rect((obj.x,obj.y),(obj.width,obj.height))
					self.platform_borders.append(border_rect)

	def platform_collision(self):
		for platform in self.platform_sprites.sprites():
			for border in self.platform_borders:
				if platform.rect.colliderect(border):
					if platform.direction.y > 0:
						platform.rect.midbottom = border.midtop
						platform.direction.y = -1
					elif platform.direction.y < 0:
						platform.rect.midtop = border.midbottom
						platform.direction.y = 1
					platform.pos.y = platform.rect.y
			if platform.rect.colliderect(self.player.rect):
				if self.player.rect.centery > platform.rect.centery:
					platform.rect.bottom = self.player.rect.top
					platform.pos.y = platform.rect.y
					platform.direction.y = -1

	def create_bullet(self,pos,direction,entity):
		Bullet(pos,self.bullet_image,direction,[self.all_sprites,self.bullet_sprites])
		FireAnimation(
			entity=entity,
			image_list=self.fire_images,
			direction=direction,
			groups=[self.all_sprites]
			)

	def bullet_collision(self):
		for obstacle in self.collision_sprites.sprites():
			pygame.sprite.spritecollide(obstacle,self.bullet_sprites,True)
		for sprite in self.vulnerable_sprites.sprites():
			if pygame.sprite.spritecollide(sprite,self.bullet_sprites,True,pygame.sprite.collide_mask):
				sprite.damage()

	def run(self):
		while True:
			dt = self.clock.tick()/1000
			for event in pygame.event.get():
				if event.type==pygame.QUIT:                              sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			self.screen.fill(BG_COLOR)
			self.platform_collision()
			self.bullet_collision()
			self.all_sprites.update(dt)
			self.all_sprites.customize_draw(self.player)
			self.overlay.display()
			pygame.display.update()

if __name__ == "__main__":
	game = Game()
=======
import pygame,sys
from settings import *
from tile     import Tile,CollisionTile,MovingPlatform
from player   import Player 
from enemy    import Enemy
from bullet   import Bullet,FireAnimation
from overlay  import Overlay
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2

class AllSprite(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.offset = Vector2(0,0)
		# SKY
		# Image
		self.fg_sky = pygame.image.load("../graphics/sky/fg_sky.png").convert_alpha()
		self.bg_sky = pygame.image.load("../graphics/sky/bg_sky.png").convert_alpha()
		tmx_map = load_pygame("../data/map.tmx")
		# Dimensions
		self.padding = WINDOW_WIDTH/2
		self.sky_width = self.bg_sky.get_width()
		map_width = tmx_map.tilewidth*tmx_map.width + 2*self.padding
		self.sky_num = int(map_width // self.sky_width)

	def customize_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		for x in range(self.sky_num):
			x_pos = -self.padding + (x*self.sky_width)
			bg_pos = Vector2(x_pos,800) - self.offset/2.5
			fg_pos = Vector2(x_pos,800) - self.offset/2
			self.screen.blit(self.bg_sky,bg_pos)
			self.screen.blit(self.fg_sky,fg_pos)
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.z):
			offset_rect = sprite.image.get_rect(center=sprite.rect.center)
			offset_rect.center -= self.offset
			self.screen.blit(sprite.image,offset_rect)

class Game:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My eighth python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		# Groups
		self.all_sprites = AllSprite()
		self.collision_sprites  = pygame.sprite.Group()
		self.platform_sprites   = pygame.sprite.Group()
		self.bullet_sprites     = pygame.sprite.Group()
		self.vulnerable_sprites = pygame.sprite.Group()
		self.setup()
		self.overlay = Overlay(self.player)
		# Image
		self.bullet_image = pygame.image.load("../graphics/bullet.png").convert_alpha()
		self.fire_images  = [
			pygame.image.load("../graphics/fire/0.png").convert_alpha(),
			pygame.image.load("../graphics/fire/1.png").convert_alpha()
			]
		# Music
		self.music =  pygame.mixer.Sound("../audio/music.ogg")
		self.music.play(loops=-1)

	def setup(self):
		tmx_map = load_pygame("../data/map.tmx")
		# Tiles
		for x,y,image in tmx_map.get_layer_by_name("Level").tiles():
			CollisionTile(
				pos=(tmx_map.tilewidth*x,tmx_map.tilewidth*y),
				image=image,
				groups=[self.all_sprites,self.collision_sprites]
				)
		for layer in ["BG","BG Detail","FG Detail Bottom","FG Detail Top"]:
			for x,y,image in tmx_map.get_layer_by_name(layer).tiles():
				Tile(
					pos=(tmx_map.tilewidth*x,tmx_map.tilewidth*y),
					image=image,
					groups=[self.all_sprites],
					z=LAYERS[layer]
					)
		# Objects
		for obj in tmx_map.get_layer_by_name("Entities"):
			match obj.name:
				case "Player":
					self.player = Player(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites,self.vulnerable_sprites],
						path="../graphics/player",
						collision_sprite=self.collision_sprites,
						create_bullet=self.create_bullet
						)
				case "Enemy":
					Enemy(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites,self.vulnerable_sprites],
						path="../graphics/enemy",
						create_bullet=self.create_bullet,
						player=self.player,
						collision_sprites=self.collision_sprites
						)
		self.platform_borders = []
		for obj in tmx_map.get_layer_by_name("Platforms"):
			match obj.name:
				case "Platform":
					MovingPlatform(
						pos=(obj.x,obj.y),
						image=obj.image,
						groups=[self.all_sprites,self.collision_sprites,self.platform_sprites]
						)
				case "Border": 
					border_rect = pygame.Rect((obj.x,obj.y),(obj.width,obj.height))
					self.platform_borders.append(border_rect)

	def platform_collision(self):
		for platform in self.platform_sprites.sprites():
			for border in self.platform_borders:
				if platform.rect.colliderect(border):
					if platform.direction.y > 0:
						platform.rect.midbottom = border.midtop
						platform.direction.y = -1
					elif platform.direction.y < 0:
						platform.rect.midtop = border.midbottom
						platform.direction.y = 1
					platform.pos.y = platform.rect.y
			if platform.rect.colliderect(self.player.rect):
				if self.player.rect.centery > platform.rect.centery:
					platform.rect.bottom = self.player.rect.top
					platform.pos.y = platform.rect.y
					platform.direction.y = -1

	def create_bullet(self,pos,direction,entity):
		Bullet(pos,self.bullet_image,direction,[self.all_sprites,self.bullet_sprites])
		FireAnimation(
			entity=entity,
			image_list=self.fire_images,
			direction=direction,
			groups=[self.all_sprites]
			)

	def bullet_collision(self):
		for obstacle in self.collision_sprites.sprites():
			pygame.sprite.spritecollide(obstacle,self.bullet_sprites,True)
		for sprite in self.vulnerable_sprites.sprites():
			if pygame.sprite.spritecollide(sprite,self.bullet_sprites,True,pygame.sprite.collide_mask):
				sprite.damage()

	def run(self):
		while True:
			dt = self.clock.tick()/1000
			for event in pygame.event.get():
				if event.type==pygame.QUIT:                              sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			self.screen.fill(BG_COLOR)
			self.platform_collision()
			self.bullet_collision()
			self.all_sprites.update(dt)
			self.all_sprites.customize_draw(self.player)
			self.overlay.display()
			pygame.display.update()

if __name__ == "__main__":
	game = Game()
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
	game.run()