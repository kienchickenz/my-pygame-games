from random import choice
from os import path
import pygame,sys
from settings import *
# Components
from game import Game
from score import Score
from preview import Preview

class Main:
	def __init__(self):
		# Defaults
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Tetris - My 16th python game")
		# Shapes
		self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]
		# Components
		self.game = Game(self.get_next_shape,self.update_score)
		self.score = Score()
		self.preview = Preview()
		# Music
		self.bg_music = pygame.mixer.Sound(path.join("..","sound","music.ogg"))
		self.bg_music.set_volume(0.06)
		self.bg_music.play(-1)

	def update_score(self,lines,score,level):
		self.score.lines = lines
		self.score.score = score
		self.score.level = level

	def get_next_shape(self):
		next_shape = self.next_shapes.pop(0)
		self.next_shapes.append(choice(list(TETROMINOS.keys())))
		return next_shape

	def run(self)->None:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					sys.exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: 
					pygame.quit()
					sys.exit()

			self.screen.fill(GRAY)
			self.game.run()
			self.score.run()
			self.preview.run(self.next_shapes)

			pygame.display.update()
			self.clock.tick(60)

if __name__ == "__main__":
	main = Main()
	main.run()