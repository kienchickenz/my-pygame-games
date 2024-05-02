from settings import *
from os import path

class Preview:
	def __init__(self):
		# Default
		self.screen = pygame.display.get_surface()
		self.preview_surface = pygame.Surface((SIZE_BAR_WIDTH,GAME_HEIGHT*PREVIEW_HEIGHT_FRACTION))
		self.preview_rect = self.preview_surface.get_rect(topright=(WINDOW_WIDTH-PADDING,PADDING))
		# Shapes
		self.shape_images = {shape:pygame.image.load(path.join("..","graphics",f"{shape}.png")).convert_alpha() 
							for shape in TETROMINOS.keys()}

	def draw_pieces(self,next_shapes):
		for index,shape in enumerate(next_shapes):
			shape_image = self.shape_images[shape]
			x = self.preview_surface.get_width()/2
			y = self.preview_surface.get_height()/6 + index * self.preview_surface.get_height()/3
			shape_rect = shape_image.get_rect(center=(x,y))
			self.preview_surface.blit(shape_image,shape_rect)

	def draw(self,next_shapes):
		self.preview_surface.fill(GRAY)
		border_rect = pygame.Rect((0,0),(self.preview_surface.get_width(),self.preview_surface.get_height()))
		pygame.draw.rect(self.preview_surface,LINE_COLOR,border_rect,2,2)
		self.draw_pieces(next_shapes)

		self.screen.blit(self.preview_surface, self.preview_rect)

	def run(self,next_shapes):
		self.draw(next_shapes)