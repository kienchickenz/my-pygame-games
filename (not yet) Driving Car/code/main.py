import pygame,sys
from settings import *
from car      import Car

class Game:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My nineth python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		# Groups
		self.all_sprites = pygame.sprite.Group()
		# Image
		self.bg_track = pygame.image.load("../graphics/track.png").convert()
		self.car = Car(groups=self.all_sprites)

	def run(self):
		while True:
			dt = self.clock.tick()/1000
			for event in pygame.event.get():
				if event.type==pygame.QUIT:                              sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()

			self.screen.blit(self.bg_track,(0,0))
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.screen)
			pygame.display.update()

if __name__ == "__main__":
	game = Game()
	game.run()