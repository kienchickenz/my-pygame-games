import pygame,sys,time
from settings import *
from sprites  import Ground,Bird,Pipe
from pygame.math import Vector2
from random import randint

class AllSprite(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.screen = pygame.display.get_surface()

	def customize_draw(self):
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.z):
			self.screen.blit(sprite.image,sprite.rect)

class Game:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My tenth python game")
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.bg = self.scale_image("../graphics/environment/day.png")
		# Groups
		self.all_sprites = AllSprite()
		self.collision_sprites = pygame.sprite.Group()
		self.pipe_sprites = pygame.sprite.Group()
		# Setup
		Ground([self.all_sprites,self.collision_sprites],self.scale_image)
		self.pipe_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.pipe_timer,1500)
		self.end_game = True
		# Score setup
		self.font = pygame.font.Font("../fonts/04B_19.ttf",40)
		self.score_text = 0
		self.high_score_text = 0
		self.score_color = "white"
		self.can_score = True
		# Screen setup
		self.end_mess = self.scale_image("../graphics/ui/end_mess.png").convert_alpha()
		self.end_mess_rect = self.end_mess.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))	
		self.end_image = self.scale_image("../graphics/ui/end_image.png").convert_alpha()
		self.end_image_rect = self.end_image.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
		# Music
		self.hit_sound = pygame.mixer.Sound("../musics/hit.ogg")
		self.hit_sound.set_volume(0.1)
		self.point_sound = pygame.mixer.Sound("../musics/point.ogg")
		self.point_sound.set_volume(0.1)

	def scale_image(self,path):
		original_image = pygame.image.load(path).convert_alpha()
		original_size = Vector2(original_image.get_width(),original_image.get_height())
		scale_factor = round(700/512,2)
		scaled_size = original_size*scale_factor
		scaled_image = pygame.transform.scale(original_image,(scaled_size))
		return scaled_image

	def collision(self):
		if self.bird.rect.top <= 0: 
			self.hit_sound.play()
			self.do_end_game()
		if pygame.sprite.spritecollide(self.bird,self.collision_sprites,False):
			if pygame.sprite.spritecollide(self.bird,self.collision_sprites,False,pygame.sprite.collide_mask):
				self.hit_sound.play()
				self.do_end_game()

	def do_end_game(self):
		self.end_game = True
		self.bird.kill()
		for sprite in self.collision_sprites:
			if sprite.sprite_type == "pipe": sprite.kill()

	def restart(self):
		self.end_game = False
		self.can_score = True
		self.score_text = 0
		self.bird = Bird(self.all_sprites,self.scale_image)

	def check_score(self):
		for sprite in self.pipe_sprites.sprites():
			if self.bird.rect.centerx - 5 < sprite.rect.centerx < self.bird.rect.centerx + 5:
				if self.can_score:
					self.score_text += 1
					self.point_sound.play()
					self.can_score = False
			if sprite.rect.centerx < 0:
				self.can_score = True 

	def draw_score(self):
		if not self.end_game:
			self.check_score()
		else:
			if self.score_text > self.high_score_text: 
				self.high_score_text = self.score_text
			high_score = self.font.render(f"High score: {self.high_score_text}",True,self.score_color)
			high_score_rect = high_score.get_rect(midbottom=(WINDOW_WIDTH/2,610))
			self.screen.blit(high_score,high_score_rect)
		score = self.font.render(f"Score: {self.score_text}",True,self.score_color)
		score_rect = score.get_rect(midtop=(WINDOW_WIDTH/2,WINDOW_HEIGHT/10))
		self.screen.blit(score,score_rect)

	def draw_menu(self):
		if self.high_score_text == 0:
			self.screen.blit(self.end_image,self.end_image_rect)
		else:
			self.screen.blit(self.end_mess,self.end_mess_rect)

	def run(self):
		prev_time = time.time()
		while True:
			# Delta time
			dt = time.time() - prev_time
			prev_time = time.time()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:                              sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
				if event.type==pygame.MOUSEBUTTONDOWN:
					if not self.end_game: 
						self.bird.jump()
					else: 
						self.restart()
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_SPACE:
						if not self.end_game:
							self.bird.jump()
						else: 
							self.restart()
				if event.type == self.pipe_timer and not self.end_game:
					pipe_x = WINDOW_WIDTH + randint(50,100)
					pipe_y = randint(150,450)
					pos = Vector2(pipe_x,pipe_y)			
					Pipe(
						[self.all_sprites,self.collision_sprites,self.pipe_sprites],
						scale_image=self.scale_image,
						pos=pos,
						orientation="down"
						)
					Pipe(
						groups=[self.all_sprites,self.collision_sprites,self.pipe_sprites],
						scale_image=self.scale_image,
						pos=pos,
						orientation="up"
						)
			self.screen.blit(self.bg,(0,0))
			if not self.end_game:
				self.all_sprites.update(dt)
				self.collision()
			else:
				self.draw_menu()
			self.all_sprites.customize_draw()
			self.draw_score()
			pygame.display.update()
			self.clock.tick(60)

if __name__ == "__main__":
	game = Game()
	game.run()