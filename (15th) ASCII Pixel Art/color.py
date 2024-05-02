import pygame
import numpy as np
import cv2

class MainProgram:
	def __init__(self, path="images/inu.jpg", font_size=12, color_lvl=8):
		pygame.init()
		self.path = path
		self.COLOR_LVL = color_lvl
		self.image, self.gray_image = self.get_image()
		self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
		self.surface = pygame.display.set_mode(self.RES)
		self.clock = pygame.time.Clock()

		self.ASCII_CHARS = ' ixzao*#MW&8%B@$'
		self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

		self.font = pygame.font.SysFont("Courier", font_size, bold=True)
		self.CHAR_STEP = int(font_size * 0.6)
		self.PALETTE, self.COLOR_COEFF = self.create_palette()

	def create_palette(self):
		colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
		color_palette = [np.array([r,g,b]) for r in colors for g in colors for b in colors]
		palette = dict.fromkeys(self.ASCII_CHARS,None)
		color_coeff = int(color_coeff)
		for char in palette:
			char_palette = {}
			for color in color_palette:
				color_key = tuple(color//color_coeff)
				char_palette[color_key] = self.font.render(char, False, tuple(color))
			palette[char] = char_palette
		return palette,color_coeff

	def get_image(self):
		self.cv2_image = cv2.imread(self.path)
		transposed_image = cv2.transpose(self.cv2_image)
		image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
		gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
		return image,gray_image

	def draw_cv2_image(self):
		resized_cv2_image = cv2.resize(self.cv2_image, (640, 640), interpolation=cv2.INTER_AREA)
		cv2.imshow("img", resized_cv2_image)

	def draw_converted_image(self):
		char_indices = self.gray_image // self.ASCII_COEFF
		color_indices = self.image // self.COLOR_COEFF
		for x in range(0, self.WIDTH, self.CHAR_STEP):
			for y in range(0, self.HEIGHT, self.CHAR_STEP):
				char_index = char_indices[x,y]
				if char_index:
					char = self.ASCII_CHARS[char_index]
					color = tuple(color_indices[x,y])
					self.surface.blit(self.PALETTE[char][color], (x,y)) 

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