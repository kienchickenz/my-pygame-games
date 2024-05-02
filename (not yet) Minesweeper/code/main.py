import pygame,sys
from settings import *
from sprites  import *
from pygame.math import Vector2
from os import walk

class Game:
	def __init__(self):
		# Defaults
		pygame.init()
		pygame.display.set_caption("My fifteenth python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		# Groups
		self.all_sprites = pygame.sprite.Group()
		# Setup
		self.images = self.import_images("../images/")
		self.board  = Board(self.all_sprites,self.images)

	def import_images(self,path):
		image_dict = {}
		for index,folder in enumerate(walk(path)):
			if index == 0:
				for key in folder[1]:
					image_dict[key] = []
			else:
				for file_name in folder[2]:
					path  = f"{folder[0]}/{file_name}"
					image = pygame.image.load(path).convert()
					scaled_image = self.scale_image(image)
					key = folder[0].split("/")[-1]
					image_dict[file_name.split(".")[0]] = scaled_image
		return image_dict

	def scale_image(self,image):
		original_size = Vector2(image.get_width(),image.get_height())
		scale_factor  = round(TILESIZE / original_size[0],2)
		scaled_size   = original_size * scale_factor
		scaled_image  = pygame.transform.scale(image,scaled_size)
		return scaled_image

	def run(self):
		self.is_playing = True
		while self.is_playing:
			self.event_loop()
			self.draw()
			pygame.display.update()
			self.clock.tick(FPS)

	def draw(self):
		self.screen.fill(BG_COLOR)
		self.all_sprites.draw(self.screen)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type==pygame.QUIT                             : sys.exit()
			if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()

if __name__ == "__main__":
	game = Game()
	game.run()