from settings import *
from os import path

class Score:
	def __init__(self):
		# Default
		self.screen = pygame.display.get_surface()
		self.score_surface = pygame.Surface((SIZE_BAR_WIDTH,GAME_HEIGHT*SCORE_HEIGHT_FRACTION-PADDING))
		self.score_rect = self.score_surface.get_rect(bottomright=(WINDOW_WIDTH-PADDING,WINDOW_HEIGHT-PADDING))
		self.font = pygame.font.Font(path.join("..","font","Russo_One.ttf"),30)
		# Data
		self.lines, self.score, self.level = 0,0,0

	def draw_text(self,pos,text):
		text_image = self.font.render(f"{text[0]}: {text[1]}",True,"white")
		text_rect = text_image.get_rect(center=pos)
		self.score_surface.blit(text_image,text_rect)

	def draw(self):
		self.score_surface.fill(GRAY)
		for index,text in enumerate([("Score",self.score),("Level",self.level),("Lines",self.lines)]):
			x = self.score_surface.get_width()/2
			y = self.score_surface.get_height()/6 + index * self.score_surface.get_height()/3
			self.draw_text((x,y),text)
		border_rect = pygame.Rect((0,0),(self.score_surface.get_width(),self.score_surface.get_height()))
		pygame.draw.rect(self.score_surface,LINE_COLOR,border_rect,2,2)

		self.screen.blit(self.score_surface,self.score_rect)

	def run(self):
		self.draw()