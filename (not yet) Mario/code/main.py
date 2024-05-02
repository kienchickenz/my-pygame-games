import pygame,sys,time
from settings import *
from level import Level

class Game:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My thirdteenth python game")
		self.clock  = pygame.time.Clock()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		# Setup
		self.level = Level(LEVEL_MAP)

	def run(self):
		prev_time = time.time()
		while True:
			# Delta time
			dt = time.time() - prev_time
			prev_time = time.time()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:                              sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			self.screen.fill("black")
			self.level.run(dt)
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == "__main__":
	game = Game()
	game.run()