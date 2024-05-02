import pygame
from pygame.image import load
from settings import *

class Menu:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.button_sprites = pygame.sprite.Group()
		self.menu_images = {}
		self.create_data()
		self.create_buttons()

	def create_data(self):
		for key,value in EDITOR_DATA.items():
			if value["menu"]:
				if not value["menu"] in self.menu_images:
					self.menu_images[value["menu"]] = [(key,load(value["menu_surf"]).convert_alpha())]
				else:
					self.menu_images[value["menu"]].append((key,load(value["menu_surf"]).convert_alpha()))

	def create_buttons(self):
		# General area
		size = 180
		margin = 6
		topleft = (WINDOW_WIDTH-size-margin,WINDOW_HEIGHT-size-margin)
		self.rect = pygame.Rect(topleft,(size,size))
		# Button area
		generic_button_rect = pygame.Rect(self.rect.topleft,(self.rect.width/2,self.rect.height/2))
		button_margin = 5
		self.tile_button_rect = generic_button_rect.copy().inflate(-button_margin,-button_margin)
		self.coin_button_rect  = generic_button_rect.copy().move(self.rect.width/2,0).inflate(-button_margin,-button_margin)
		self.palm_button_rect  = generic_button_rect.copy().move(0,self.rect.height/2).inflate(-button_margin,-button_margin)
		self.enemy_button_rect = generic_button_rect.copy().move(self.rect.width/2,self.rect.height/2).inflate(-button_margin,-button_margin)
		# Create button
		Button(self.tile_button_rect,self.button_sprites,self.menu_images["terrain"])
		Button(self.coin_button_rect,self.button_sprites,self.menu_images["coin"])
		Button(self.palm_button_rect,self.button_sprites,self.menu_images["palm fg"],self.menu_images["palm bg"])
		Button(self.enemy_button_rect,self.button_sprites,self.menu_images["enemy"])

	def click(self,mouse_pos,mouse_button):
		for button in self.button_sprites:
			if button.rect.collidepoint(mouse_pos):
				if mouse_button[1]:
					if button.items["alt"]:
						button.main_active = not button.main_active
				if mouse_button[2]:
					button.switch()
				return button.get_id()

	def highlight_indicator(self,index):
		match EDITOR_DATA[index]["menu"]: 
			case "terrain":
				pygame.draw.rect(self.screen,BUTTON_LINE_COLOR,self.tile_button_rect.inflate(4,4),5,4)
			case "coin":
				pygame.draw.rect(self.screen,BUTTON_LINE_COLOR,self.coin_button_rect.inflate(4,4),5,4)
			case "enemy":
				pygame.draw.rect(self.screen,BUTTON_LINE_COLOR,self.enemy_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]["menu"] in ("palm bg","palm fg"):
			pygame.draw.rect(self.screen,BUTTON_LINE_COLOR,self.palm_button_rect.inflate(4,4),5,4)

	def display(self,index):
		self.button_sprites.update()
		self.button_sprites.draw(self.screen)
		self.highlight_indicator(index)
		
class Button(pygame.sprite.Sprite):
	def __init__(self,rect,groups,items,items_alt=None):
		super().__init__(groups)
		self.image = pygame.Surface(rect.size)
		self.rect = rect
		# Items
		self.items = {"main":items,"alt":items_alt}
		self.main_active = True
		self.index = 0

	def get_id(self):
		return self.items["main" if self.main_active else "alt"][self.index][0]
 
	def switch(self):
 		self.index += 1
 		if self.index >= len(self.items["main" if self.main_active else "alt"]):
 			self.index = 0

	def update(self):
		self.image.fill(BUTTON_BG_COLOR)
		image = self.items["main" if self.main_active else "alt"][self.index][1]
		rect  = image.get_rect(center=(self.rect.width/2,self.rect.height/2))
		self.image.blit(image,rect)