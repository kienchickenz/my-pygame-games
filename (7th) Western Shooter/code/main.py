import pygame,sys
from settings import *
from player   import Player
from monster  import Coffin,Cactus
from sprite   import Sprite,Bullet
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame
class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = Vector2(0,0)
		self.screen = pygame.display.get_surface()
		self.bg     = pygame.image.load("../graphics/other/bg.png").convert()

	def customize_draw(self,player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
		self.screen.blit(self.bg,-self.offset)
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
			offset_rect = sprite.image.get_rect(center=sprite.rect.center)
			offset_rect.center -= self.offset
			self.screen.blit(sprite.image,offset_rect)

class Game:
	def __init__(self):
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My seventh python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		self.bullet_image = pygame.image.load("../graphics/other/particle.png").convert_alpha()
		self.all_sprites = AllSprites()
		self.obstacles   = pygame.sprite.Group() 
		self.bullets     = pygame.sprite.Group()
		self.monsters    = pygame.sprite.Group()
		self.setup()
		self.bg_music = pygame.mixer.Sound("../musics/music.ogg")
		self.bg_music.play(loops=-1)

	def create_bullet(self,pos,direction):
		Bullet(pos,direction,self.bullet_image,[self.all_sprites,self.bullets])

	def bullet_collision(self):
		# With obstacles
		for obstacle in self.obstacles.sprites():
			if pygame.sprite.spritecollide(obstacle,self.bullets,dokill=False):
				pygame.sprite.spritecollide(obstacle,self.bullets,True,pygame.sprite.collide_mask)
		# With monsters
		for monster in self.monsters.sprites():
			if pygame.sprite.spritecollide(monster,self.bullets,dokill=False):
				if pygame.sprite.spritecollide(monster,self.bullets,True,pygame.sprite.collide_mask):
					monster.damage()
		# With player
		if pygame.sprite.spritecollide(self.player,self.bullets,dokill=False):
			if pygame.sprite.spritecollide(self.player,self.bullets,True,pygame.sprite.collide_mask):
				self.player.damage()

	def setup(self):
		tmx_map = load_pygame("../data/map_ex.tmx")
		# Tiles
		for x,y,image in tmx_map.get_layer_by_name("Fence").tiles():
			Sprite((x*64,y*64),image,[self.all_sprites,self.obstacles])
		# Objects
		for obj in tmx_map.get_layer_by_name("Objects"):
			Sprite((obj.x,obj.y),obj.image,[self.all_sprites,self.obstacles])
		for obj in tmx_map.get_layer_by_name("Entities"):
			match obj.name:
				case "Player":
					self.player = Player(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites],
						path=PATHS["player"],
						collision_sprites=self.obstacles,
						create_bullet=self.create_bullet
						)
				case "Coffin":
					Coffin(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites,self.monsters],
						path=PATHS["coffin"],
						collision_sprites=self.obstacles,
						player=self.player
						)
				case "Cactus":
					Cactus(
						pos=(obj.x,obj.y),
						groups=[self.all_sprites,self.monsters],
						path=PATHS["cactus"],
						collision_sprites=self.obstacles,
						player=self.player,
						create_bullet=self.create_bullet
						)

	def run(self):
		while True:
			dt = self.clock.tick()/1000
			for event in pygame.event.get():
				if event.type==pygame.QUIT                             : sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			self.screen.fill("grey22")
			self.all_sprites.update(dt)
			self.bullet_collision()
			self.all_sprites.customize_draw(self.player)
			pygame.display.update()

if __name__ == "__main__":
	game = Game()
	game.run()