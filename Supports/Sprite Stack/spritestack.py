import pygame

import sys
import os

class Game:
	def __init__(self):
		# Default
		pygame.init()
		pygame.display.set_caption("Sprite Stack")
		self.screen = pygame.display.set_mode((500,500),0,32)
		self.display = pygame.Surface((100,100))
		self.clock = pygame.Clock()
		# Setup
		self.image_list = [pygame.image.load(f"car/{image_name}").convert_alpha() 
							for image_name in os.listdir("car")]

	def render_stack(self,surf,images,pos,rotation,spread=1):
		for index,image in enumerate(images):
			rotated_image = pygame.transform.rotate(image,rotation)
			surf.blit(rotated_image,(pos[0] - rotated_image.get_width() // 2, pos[1] - rotated_image.get_height() // 2 - index * spread))

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_q: 
					pygame.quit()
					sys.exit()
			
			self.screen.fill("pink")
			self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
			self.render_stack(self.display,self.image_list,(50,50),)

			pygame.display.update()
			self.clock.tick(60)

if __name__ == "__main__":
	game = Game()
	game.run()