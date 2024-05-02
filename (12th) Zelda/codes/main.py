import pygame,sys,time
from settings import *
from level import Level

class Game:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My twelve python game")
		self.clock  = pygame.time.Clock()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		# Setup
		self.level = Level()
		# Sound
		self.bg_sound = pygame.mixer.Sound("../musics/main.ogg")
		self.bg_sound.set_volume(0.5)
		self.bg_sound.play(loops=-1)

	def run(self):
		prev_time = time.time()
		while True:
			# Delta 
			dt = time.time() - prev_time
			prev_time = time.time()
			for event in pygame.event.get():
				if event.type==pygame.QUIT                                                          : sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_m:
						self.level.upgrade_menu()
			self.screen.fill(WATER_COLOR)
			self.level.run(dt)
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == "__main__":
	game = Game()
	game.run()			