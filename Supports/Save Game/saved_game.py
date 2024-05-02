import pygame,sys
import json
from pygame.math import Vector2
from settings import *

class Game:
	def __init__(self):
		# Defaults
		pygame.init()
		pygame.display.set_caption("Saved game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock  = pygame.time.Clock()
		# Data
		self.data = {
			"Rect 1":0,
			"Rect 2":0
		}
		try:
			with open("saved_data.txt") as score_file:
				self.data = json.load(score_file)
		except:
			pass
		self.rect1_score = self.data['Rect 1']
		self.rect2_score = self.data['Rect 2']
		# Setup
		self.font = pygame.font.Font(None,32)
		self.setup()

	def setup(self):
		self.rect1 = pygame.Surface((SIZE,SIZE))
		self.rect1.fill(RED)
		self.rect1_rect = self.rect1.get_rect(center=(WINDOW_WIDTH/2-SIZE/2-50,WINDOW_HEIGHT/2))
		self.rect2 = pygame.Surface((SIZE,SIZE))
		self.rect2.fill(BLUE)
		self.rect2_rect = self.rect2.get_rect(center=(WINDOW_WIDTH/2+SIZE/2+50,WINDOW_HEIGHT/2))

	def draw(self):
		self.rect1_text = self.font.render(f"Clicks: {self.rect1_score}",True,"black")
		self.rect1_text_rect = self.rect1_text.get_rect(midtop=(Vector2(self.rect1_rect.midbottom)+Vector2(0,10)))
		self.rect2_text = self.font.render(f"Clicks: {self.rect2_score}",True,"black")
		self.rect2_text_rect = self.rect1_text.get_rect(midtop=(Vector2(self.rect2_rect.midbottom)+Vector2(0,10)))
		self.screen.blit(self.rect1,self.rect1_rect)
		self.screen.blit(self.rect2,self.rect2_rect)
		self.screen.blit(self.rect1_text,self.rect1_text_rect)
		self.screen.blit(self.rect2_text,self.rect2_text_rect)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT                               : self.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_q: self.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.rect1_rect.collidepoint(event.pos):
						self.rect1_score += 1
					elif self.rect2_rect.collidepoint(event.pos):
						self.rect2_score += 1
			# Draw
			self.screen.fill((245,255,252))
			self.draw()
			pygame.display.update()
			self.clock.tick(60)

	def exit(self):
		with open("saved_data.txt","w") as score_file:
			self.data["Rect 1"] = self.rect1_score
			self.data["Rect 2"] = self.rect2_score
			json.dump(self.data,score_file)
		sys.exit()

if __name__ == "__main__":
	game = Game()
	game.run()