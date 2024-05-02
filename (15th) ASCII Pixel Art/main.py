import pygame
import numpy as np
import pygame.gfxdraw
import cv2

class MainProgram:
	def __init__(self, path="images/inu.jpg", pixel_size=7, color_lvl=8):
		pygame.init()
		self.path = path
		self.PIXEL_SIZE = pixel_size
		self.COLOR_LVL = color_lvl
		self.image = self.get_image()
		self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
		self.surface = pygame.display.set_mode(self.RES)
		self.clock = pygame.time.Clock()
		self.PALETTE, self.COLOR_COEFF = self.create_palette()

	def create_palette(self):
		colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
		color_palette = [np.array([r,g,b]) for r in colors for g in colors for b in colors]
		palette = {}
		color_coeff = int(color_coeff)
		for color in color_palette:
			color_key = tuple(color//color_coeff)
			palette[color_key] = color
		return palette,color_coeff

	def get_image(self):
		self.cv2_image = cv2.imread(self.path)
		transposed_image = cv2.transpose(self.cv2_image)
		image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
		return image

	def draw_cv2_image(self):
		resized_cv2_image = cv2.resize(self.cv2_image, (640, 640), interpolation=cv2.INTER_AREA)
		cv2.imshow("img", resized_cv2_image)

	def draw_converted_image(self):
		color_indices = self.image // self.COLOR_COEFF
		for x in range(0, self.WIDTH, self.PIXEL_SIZE):
			for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
				color_key = tuple(color_indices[x,y])
				if sum(color_key):
					color = self.PALETTE[color_key]
					pygame.gfxdraw.box(self.surface, (x,y,self.PIXEL_SIZE,self.PIXEL_SIZE), color)

	def draw(self):
		self.surface.fill("black")
		self.draw_converted_image()
		self.draw_cv2_image()

	def save_image(self):
		pygame_image = pygame.surfarray.array3d(self.surface)
		cv2_img = cv2.transpose(pygame_image)
		cv2.imwrite("output/converted_image.png", cv2_img)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT: exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_q: exit()
				if event.type==pygame.KEYDOWN and event.key==pygame.K_s: self.save_image()
			self.draw()
			pygame.display.set_caption(str(self.clock.get_fps()))
			pygame.display.flip()
			self.clock.tick()

if __name__ == "__main__":
	program = MainProgram()
	program.run()