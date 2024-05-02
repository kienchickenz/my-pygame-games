import pygame,sys
from pygame.math import Vector2
from random      import choice,randint

from settings import *
from support  import *
from sprites  import Generic,Animated,Particle,Coin,Block,Cloud
from player   import Player
from enemies  import Spikes,Tooth,Shell

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.offset = Vector2()

	def draw_horizon(self):
		horizon_pos = self.horizon_y - self.offset.y
		# Sea
		sea_rect = pygame.Rect((0,horizon_pos),(WINDOW_WIDTH,WINDOW_HEIGHT-horizon_pos))
		pygame.draw.rect(self.screen,SEA_COLOR,sea_rect)
		# Horizon lines
		horizon_rect_1 = pygame.Rect((0,horizon_pos-10),(WINDOW_WIDTH,10))
		horizon_rect_2 = pygame.Rect((0,horizon_pos-16),(WINDOW_WIDTH,4))
		horizon_rect_3 = pygame.Rect((0,horizon_pos-20),(WINDOW_WIDTH,2))
		pygame.draw.rect(self.screen,HORIZON_TOP_COLOR,horizon_rect_1)
		pygame.draw.rect(self.screen,HORIZON_TOP_COLOR,horizon_rect_2)
		pygame.draw.rect(self.screen,HORIZON_TOP_COLOR,horizon_rect_3)
		pygame.draw.line(self.screen,HORIZON_COLOR,(0,horizon_pos),(WINDOW_WIDTH,horizon_pos),3)

	def custom_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		for sprite in self:
			if sprite.z == LEVEL_LAYERS["clouds"]:
				offset_rect = sprite.rect.copy()
				offset_rect.center -= self.offset
				self.screen.blit(sprite.image,offset_rect)
		self.draw_horizon()
		for layer in LEVEL_LAYERS.values():	
			for sprite in self:
				if sprite.z == layer and sprite.z != LEVEL_LAYERS["clouds"]:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.screen.blit(sprite.image,offset_rect)

class Level:
	def __init__(self,grid,switch,asset_dict,music):
		self.screen = pygame.display.get_surface()
		self.switch = switch
		# Groups
		self.all_sprites       = CameraGroup()
		self.coin_sprites      = pygame.sprite.Group()
		self.damage_sprites    = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.shell_sprites     = pygame.sprite.Group()
		self.build_level(grid,asset_dict,music["jump"])
		# Limits
		# Error if there isn't any terrain tile
		self.level_limits = {
			"left" :-WINDOW_WIDTH,
			"right":sorted(list(grid["terrain"].keys()),key=lambda pos:pos[0])[-1][0] + 600
		}
		self.particle_images = asset_dict["particle"]
		# Clouds
		self.cloud_images = asset_dict["cloud"]
		self.cloud_timer = pygame.USEREVENT + 2
		pygame.time.set_timer(self.cloud_timer,2000)
		self.startup_clouds()
		# Music
		self.bg_music = music["music"]
		self.bg_music.set_volume(0.4)
		self.bg_music.play(loops=-1)
		self.coin_sound = music["coin"]
		self.coin_sound.set_volume(0.3)
		self.hit_sound = music["hit"]
		self.hit_sound.set_volume(0.3)

	def build_level(self,grid,asset_dict,jump_sound):
		for layer_name,layer in grid.items():
			for pos,data in layer.items():
				if layer_name == "terrain":
					Generic([self.all_sprites,self.collision_sprites],pos,asset_dict["land"][data])
				if layer_name == "water":
					if data == "top":
						Animated(self.all_sprites,pos,asset_dict["water top"],z=LEVEL_LAYERS["water"])
					else:
						Generic(self.all_sprites,pos,asset_dict["water bottom"],z=LEVEL_LAYERS["water"])
				match data:
					case 0 : self.player = Player(self.all_sprites,pos,asset_dict["player"],self.collision_sprites,jump_sound)
					case 1 :
						self.horizon_y = pos[1]
						self.all_sprites.horizon_y = pos[1]
					# Coins
					case 4 : Coin([self.all_sprites,self.coin_sprites],pos,asset_dict["gold"],"gold")
					case 5 : Coin([self.all_sprites,self.coin_sprites],pos,asset_dict["silver"],"silver")
					case 6 : Coin([self.all_sprites,self.coin_sprites],pos,asset_dict["diamond"],"diamond")
					# Enemies
					case 7 : Spikes([self.all_sprites,self.damage_sprites],pos,asset_dict["spikes"])
					case 8 : 
						Tooth([self.all_sprites,self.damage_sprites],pos,asset_dict["tooth"],self.collision_sprites)
					case 9 : 
						Shell(
							groups=[self.all_sprites,self.collision_sprites,self.shell_sprites],
							pos=pos,
							images=asset_dict["shell"],
							orientation="left",
							pearl_image=asset_dict["pearl"],
							damage_sprites= self.damage_sprites
							)
					case 10: 
						Shell(
							groups=[self.all_sprites,self.collision_sprites,self.shell_sprites],
							pos=pos,
							images=asset_dict["shell"],
							orientation="right",
							pearl_image=asset_dict["pearl"],
							damage_sprites= self.damage_sprites
							)
					# Palm trees
					case 11: 
						Animated(self.all_sprites,pos,asset_dict["palms"]["small_fg"])
						Block([self.collision_sprites],pos,(80,50))
					case 12: 
						Animated(self.all_sprites,pos,asset_dict["palms"]["large_fg"])
						Block([self.collision_sprites],pos,(80,50))
					case 13: 
						Animated(self.all_sprites,pos,asset_dict["palms"]["left_fg"])
						Block([self.collision_sprites],pos,(80,50))
					case 14: 
						Animated(self.all_sprites,pos,asset_dict["palms"]["right_fg"])
						Block([self.collision_sprites],pos+Vector2(50,0),(80,50))
					
					case 15: Animated(self.all_sprites,pos,asset_dict["palms"]["small_bg"],z=LEVEL_LAYERS["bg"])
					case 16: Animated(self.all_sprites,pos,asset_dict["palms"]["large_bg"],z=LEVEL_LAYERS["bg"])
					case 17: Animated(self.all_sprites,pos,asset_dict["palms"]["left_bg"] ,z=LEVEL_LAYERS["bg"])
					case 18: Animated(self.all_sprites,pos,asset_dict["palms"]["right_bg"],z=LEVEL_LAYERS["bg"])
		for sprite in self.shell_sprites:
			sprite.player = self.player

	def get_coins(self):
		collided_coins = pygame.sprite.spritecollide(self.player,self.coin_sprites,True)
		for coin in collided_coins:
			Particle(self.all_sprites,coin.rect.center,self.particle_images)
			self.coin_sound.play()

	def get_damage(self):
		collision_sprites = pygame.sprite.spritecollide(self.player,self.damage_sprites,False,pygame.sprite.collide_mask)
		if collision_sprites:
			self.player.damage()
			self.hit_sound.play()

	def create_clouds(self,event):
		if event.type == self.cloud_timer:
			image = choice(self.cloud_images)
			image = pygame.transform.scale2x(image) if randint(0,5) > 3 else image
			pos_x = self.level_limits["right"] + randint(100,300)
			pos_y = self.horizon_y - randint(0,800)
			Cloud(self.all_sprites,(pos_x,pos_y),image,self.level_limits["left"])

	def startup_clouds(self):
		for i in range(40):
			image = choice(self.cloud_images)
			image = pygame.transform.scale2x(image) if randint(0,5) > 3 else image
			pos_x = randint(self.level_limits["left"],self.level_limits["right"])
			pos_y = self.horizon_y - randint(0,800)
			Cloud(self.all_sprites,(pos_x,pos_y),image,self.level_limits["left"])

	def event_loop(self):
		for event in pygame.event.get():
			if event.type==pygame.QUIT                             : sys.exit()
			if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					self.switch()
					self.bg_music.stop()
			self.create_clouds(event)

	def run(self,dt):
		# Update
		self.event_loop()
		self.all_sprites.update(dt)
		self.get_coins()
		self.get_damage()
		# Draw
		self.screen.fill(SKY_COLOR)
		self.all_sprites.custom_draw(self.player)