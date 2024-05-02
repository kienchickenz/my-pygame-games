import pygame,sys,time
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder

from settings import *

class PathFinder:
	def __init__(self,screen,matrix,player):
		self.screen = screen
		self.matrix = matrix
		self.grid = Grid(matrix=matrix)
		self.select_image = pygame.image.load("../graphic/selection.png").convert_alpha()
		# Pathfinding
		self.path = []
		self.player = player

	def create_path(self)->None:
		# Start
		start_x,start_y = self.player.get_coord()
		start = self.grid.node(start_x,start_y)
		# End
		end_x,end_y = self.get_current_cell()[0],self.get_current_cell()[1]
		end = self.grid.node(end_x,end_y)
		# Path
		finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
		self.path = finder.find_path(start,end,self.grid)[0]
		self.grid.cleanup()
		self.player.set_path(self.path,True)

	def draw_path(self)->None:
		if len(self.path) > 2:
			points = []
			for index,point in enumerate(self.path):
				x = point.x * CELL_SIZE + CELL_SIZE / 2
				y = point.y * CELL_SIZE + CELL_SIZE / 2
				points.append((x,y))
				pygame.draw.circle(self.screen,LINE_COLOR,(x,y),2)
			pygame.draw.lines(self.screen,LINE_COLOR,False,points,5)

	def draw_active_cell(self)->None:
		col,row = self.get_current_cell()[0],self.get_current_cell()[1]
		if self.matrix[row][col] == 1:
			rect = pygame.Rect((CELL_SIZE * col,CELL_SIZE * row),(32,32))
			self.screen.blit(self.select_image,rect)

	def get_current_cell(self)->tuple:
		mouse_pos = pygame.mouse.get_pos()
		col = mouse_pos[0] // CELL_SIZE
		row = mouse_pos[1] // CELL_SIZE
		return (col,row)

	def update(self)->None:
		self.draw_active_cell()
		self.draw_path()

class Player(pygame.sprite.Sprite):
	def __init__(self,group):
		super().__init__(group)
		self.image = pygame.image.load("../graphic/roomba.png").convert_alpha()
		self.rect  = self.image.get_rect(topleft=(CELL_SIZE,CELL_SIZE))
		# Movement
		self.pos = self.rect.center
		self.speed = 150
		self.direction = pygame.math.Vector2(0,0)
		# Path
		self.collision_rects = []

	def get_coord(self)->tuple:
		return self.rect.centerx//CELL_SIZE,self.rect.centery//CELL_SIZE

	def create_collision_rects(self,path)->None:
		self.collision_rects = []
		for point in path:
			x = point.x * 32 + 16 - 2
			y = point.y * 32 + 16 - 2
			rect = pygame.Rect((x,y),(4,4))
			self.collision_rects.append(rect)

	def get_direction(self,remove_first_point = False)->None:
		if remove_first_point: self.collision_rects.remove(self.collision_rects[0])
		if len(self.collision_rects) >= 1:
			start = pygame.math.Vector2(self.pos)
			end = pygame.math.Vector2(self.collision_rects[0].center)
			self.direction = (end - start).normalize()
		elif len(self.collision_rects) == 0:
			self.direction = pygame.math.Vector2(0,0)

	def set_path(self,path,remove_first_point)->None:
		if path:
			self.create_collision_rects(path)
			self.get_direction(remove_first_point)

	def collision(self)->None:
		if self.collision_rects:
			for rect in self.collision_rects:
				if rect.collidepoint(self.pos):
					self.collision_rects.remove(self.collision_rects[0])
					self.get_direction()

	def update(self,dt)->None:
		self.collision()
		self.pos += self.direction * self.speed * dt
		self.rect.center = self.pos

class Game:
	def __init__(self):
		pygame.init()
		# Defaults
		pygame.display.set_caption("Pathfinding")
		pygame.mouse.set_visible(False)
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.Clock()
		# Setup
		self.bg = pygame.image.load("../graphic/map.png").convert()
		self.all_sprites = pygame.sprite.Group()
		self.player = Player(self.all_sprites)
		self.pathfinder = PathFinder(self.screen,MAP_MATRIX,self.player)

	def run(self)->None:
		prev_time = time.time()
		while True:
			dt = time.time() - prev_time
			prev_time = time.time()
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.pathfinder.create_path()
			# Draw
			self.screen.fill("orange")
			self.screen.blit(self.bg,(0,0))
			self.all_sprites.draw(self.screen)

			# Update
			self.pathfinder.update()
			self.all_sprites.update(dt)

			pygame.display.update()
			self.clock.tick(60)

if __name__ == "__main__":
	game = Game()
	game.run()