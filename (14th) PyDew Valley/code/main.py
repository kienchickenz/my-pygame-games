import pygame,sys
from settings import *
from level    import Level

class Game:
	def __init__(self):
		# Defaults
		pygame.init()
		pygame.display.set_caption("My fourteen python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT                             : sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()

if __name__ == "__main__":
	game = Game()
	game.run()