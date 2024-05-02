import pygame
from settings import *
from copy import deepcopy
from random import choice,randrange

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH * TILESIZE, HEIGHT * TILESIZE), pygame.NOFRAME)
		self.clock = pygame.time.Clock()
		self.grid = [pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE) for x in range(WIDTH) for y in range(HEIGHT)]
		self.figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in figure_pos] for figure_pos in FIGURE_POS]
		self.figure_rect = pygame.Rect(0, 0, TILESIZE, TILESIZE)
		self.figure = deepcopy(choice(self.figures))
		self.dx = 0
		self.can_move = False
		self.animation_count, self.animation_speed, self.animation_limit = 0,60,2000 
		self.field = [[0 for i in range(WIDTH)] for j in range(HEIGHT + 1)]

	def inputs(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]: 
			self.dx = -1
			self.can_move = True
		if keys[pygame.K_RIGHT]: 
			self.dx = 1
			self.can_move = True
		if keys[pygame.K_DOWN]:
			self.animation_limit = 100
		if keys[pygame.K_UP]:
			self.can_rotate = True

	def check_borders(self, figure):
		if figure.x < 0 or figure.x > WIDTH - 1: return True
		if figure.y > HEIGHT - 1 or self.field[figure.y][figure.x]: return True
		return False

	def update(self):
		self.prev_figure = deepcopy(self.figure)
		if self.can_move:
			for i in range(4):
				self.figure[i].x += self.dx
				if self.check_borders(self.figure[i]):
					self.figure = deepcopy(self.prev_figure)
					break
		self.animation_count += self.animation_speed
		if self.animation_count >= self.animation_limit: 
			self.animation_count = 0
			for i in range(4):
				self.figure[i].y += 1
				if self.check_borders(self.figure[i]):
					for i in range(4):
						self.field[self.prev_figure[i].y][self.prev_figure[i].x] = "pink"
					self.figure = deepcopy(choice(self.figures))
					self.animation_limit = 2000
					break

	def draw(self):
		self.screen.fill("orange")
		for i in range(4):
			self.figure_rect.x = self.figure[i].x * TILESIZE
			self.figure_rect.y = self.figure[i].y * TILESIZE
			pygame.draw.rect(self.screen, BLOCK_COLOR, self.figure_rect)
		for y,row in enumerate(self.field):
			for x,col in enumerate(row):
				if col:
					self.figure_rect.x, self.figure_rect.y = x * TILESIZE, y * TILESIZE
					pygame.draw.rect(self.screen, col, self.figure_rect)
		[pygame.draw.rect(self.screen, GRID_COLOR, i_rect, 1) for i_rect in self.grid]

	def run(self):
		while True:
			self.can_move = False
			self.can_rotate = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT: exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: exit()
					self.inputs()
			
			self.update()
			self.draw()

			pygame.display.update()
			self.clock.tick(60)

if __name__ == "__main__":
	game = Game()
	game.run()