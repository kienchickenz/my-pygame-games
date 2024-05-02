import pygame,sys,time
from settings import *
from sprites import Player,Laser,Block,Alien,ExtraAlien
from pygame.math import Vector2
from random import choice,randint

class Game:
	def __init__(self):
		# Defaults
		super().__init__()
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My eleventh python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		# Groups
		self.all_sprites          = pygame.sprite.Group()
		self.obstacle_sprites     = pygame.sprite.Group()
		self.alien_sprites        = pygame.sprite.Group()
		self.laser_sprites        = pygame.sprite.Group()
		self.extra_alien_sprites  = pygame.sprite.Group()
		self.alien_laser_sprites  = pygame.sprite.Group()
		self.player_laser_sprites = pygame.sprite.Group()
		# Image setup
		self.player_image = pygame.image.load("../graphics/others/player.png").convert_alpha()
		# Player setup
		self.player = Player(
						groups=self.all_sprites,
						image= self.player_image,
						pos=(WINDOW_WIDTH/2,WINDOW_HEIGHT),
						create_laser=self.create_laser
							)
		# Obstacles setup
		self.obstacle_numbers = 4
		self.obstacle_setup()
		# Aliens setup
		self.alien_setup()
		self.alien_direction = Vector2(1,0)
		self.ALIEN_LASER = pygame.USEREVENT + 1
		pygame.time.set_timer(self.ALIEN_LASER,500)
		self.extra_alien_time = randint(600,1000)
		# Score setup
		self.font = pygame.font.Font("../fonts/Pixeled.ttf",20)
		self.score_text = 0
		self.score_color = "white"
		self.crt = CRT()
		# Music
		self.laser_sound = pygame.mixer.Sound("../musics/laser.ogg")
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound("../musics/explosion.ogg")
		self.explosion_sound.set_volume(0.3)
		self.music = pygame.mixer.Sound("../musics/music.ogg")
		self.music.set_volume(0.2)
		self.music.play(loops=-1)

	def create_laser(self,pos,entity):
		if entity == "Alien":
			Laser([self.all_sprites,self.alien_laser_sprites],pos,entity)
		elif entity == "Player":
			Laser([self.all_sprites,self.player_laser_sprites],pos,entity)
			self.laser_sound.play()

	def obstacle_setup(self):
		x_offset = WINDOW_WIDTH/self.obstacle_numbers
		y_offset = WINDOW_HEIGHT - 120
		offset = Vector2(x_offset,y_offset)
		x_start = (WINDOW_WIDTH/self.obstacle_numbers - len(OBSTACLE_SHAPE[0]) * BLOCK_SIZE)/2
		for i in range(self.obstacle_numbers):
			for row_index,row in enumerate(OBSTACLE_SHAPE):
				for col_index,col in enumerate(row):
					if col != " ":
						x = col_index * BLOCK_SIZE + offset.x * i + x_start
						y = row_index * BLOCK_SIZE + offset.y
						pos = (x,y)
						Block([self.all_sprites,self.obstacle_sprites],pos)

	def alien_setup(self):
		x_offset = (WINDOW_WIDTH - 60 * len(ALIEN_MAP[0]))/2
		y_offset = 75
		offset = Vector2(x_offset,y_offset)
		for row_index,row in enumerate(ALIEN_MAP):
			for col_index,col in enumerate(row):
				x = col_index * 60 + offset.x
				y = row_index * 50 + offset.y
				pos = (x,y)
				Alien(
					groups=[self.all_sprites,self.alien_sprites],
					color=COLOR_LEGEND[col],
					pos=pos
					)

	def alien_movement(self,dt):
		for sprite in self.alien_sprites.sprites():
			if sprite.rect.left < 0:
				self.alien_direction.x = 1
				self.alien_movedown(dt)
			elif sprite.rect.right > WINDOW_WIDTH:
				self.alien_direction.x = -1
				self.alien_movedown(dt)
			sprite.move(dt,self.alien_direction)

	def alien_movedown(self,dt):
		for sprite in self.alien_sprites.sprites():
			self.alien_direction.y = 40
			sprite.move(dt,self.alien_direction)
		self.alien_direction.y = 0

	def alien_shoot(self):
		if self.alien_sprites.sprites():
			alien = choice(self.alien_sprites.sprites())
			self.create_laser(alien.rect.center,"Alien")

	def extra_alien(self):
		self.extra_alien_time -= 1
		if self.extra_alien_time <= 0:
			ExtraAlien([self.all_sprites,self.extra_alien_sprites],choice(["right","left"]))
			self.extra_alien_time = randint(1000,1200)

	def collision(self):
		# Player laser
		for laser in self.player_laser_sprites.sprites():
			# With obstacles
			if pygame.sprite.spritecollide(laser,self.obstacle_sprites,True):
				laser.kill()
			# With aliens
			aliens_hit = pygame.sprite.spritecollide(laser,self.alien_sprites,False)
			if aliens_hit:
				if pygame.sprite.spritecollide(laser,self.alien_sprites,True,pygame.sprite.collide_mask):
					laser.kill()
					self.explosion_sound.play()
					for alien in aliens_hit: self.score_text += alien.value

			if pygame.sprite.spritecollide(laser,self.extra_alien_sprites,False):
				if pygame.sprite.spritecollide(laser,self.extra_alien_sprites,True,pygame.sprite.collide_mask):
					laser.kill()
					self.explosion_sound.play()
					self.score_text += 500
		# Alien laser
		for laser in self.alien_laser_sprites.sprites():
			# With obstacles
			if pygame.sprite.spritecollide(laser,self.obstacle_sprites,True):
				laser.kill()
			# With player
		if pygame.sprite.spritecollide(self.player,self.alien_laser_sprites,False):
			if pygame.sprite.spritecollide(self.player,self.alien_laser_sprites,True,pygame.sprite.collide_mask):
				self.player.damage()
		# Alien
		for alien in self.alien_sprites.sprites():
			# With obstacles
			if pygame.sprite.spritecollide(alien,self.obstacle_sprites,False):
				pygame.sprite.spritecollide(alien,self.obstacle_sprites,True,pygame.sprite.collide_mask)
			# With player
		if pygame.sprite.spritecollide(self.player,self.alien_sprites,False):
			if pygame.sprite.spritecollide(self.player,self.alien_sprites,False,pygame.sprite.collide_mask):
				sys.exit()

	def display_lives(self):
		pos_x = WINDOW_WIDTH - (self.player.image.get_width() + 10) * (self.player.lives - 1)
		pos_y = 10	
		pos = Vector2(pos_x,pos_y)		
		for i in range(self.player.lives-1):
			if i != 0:
				pos.x = pos.x + self.player.image.get_width() + 10
			self.screen.blit(self.player_image,pos) 

	def display_scores(self):
		self.score = self.font.render(f"SCORE: {self.score_text}",True,self.score_color)
		self.score_rect = self.score.get_rect(topleft=(10,-10))
		self.screen.blit(self.score,self.score_rect)

	def display_victory_mess(self):
		if not self.alien_sprites.sprites():
			victory = self.font.render("YOU WON!",True,"white")
			victory_rect = victory.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
			self.screen.blit(victory,victory_rect)

	def run(self):
		prev_time = time.time()
		while True:
			# Delta time
			dt = time.time() - prev_time
			prev_time = time.time()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:                              sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
				if event.type==self.ALIEN_LASER:
					self.alien_shoot()
			# Draw
			self.screen.fill((30,30,30))
			self.all_sprites.draw(self.screen)
			self.display_lives()
			self.display_scores()
			self.crt.draw()
			self.display_victory_mess()
			# Update
			self.all_sprites.update(dt)
			self.alien_movement(dt)
			self.extra_alien()
			self.collision()
			pygame.display.update()

class CRT:
	def __init__(self):
		image = pygame.image.load("../graphics/others/tv.png").convert_alpha()
		self.scaled_image = pygame.transform.scale(image,(WINDOW_WIDTH,WINDOW_HEIGHT))
		self.rect  = self.scaled_image.get_rect(topleft=(0,0))
		self.screen = pygame.display.get_surface()
		self.create_crt_lines()

	def create_crt_lines(self):
		line_height = 3
		line_width = 1
		line_numbers = WINDOW_HEIGHT // line_height
		for i in range(line_numbers):
			pos_y = i * line_height
			pygame.draw.line(
				self.scaled_image,
				(20,20,20),
				(0,pos_y),
				(WINDOW_WIDTH,pos_y),
				line_width
				)

	def draw(self):
		self.scaled_image.set_alpha(randint(60,75))
		self.screen.blit(self.scaled_image,self.rect)

if __name__ == "__main__":
	game = Game()
	game.run()