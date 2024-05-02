import pygame
from settings import *

class UI:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
		# Bar setup
		self.health_bar_rect = pygame.Rect((10,10),(HEALTH_BAR_WIDTH,BAR_HEIGHT))
		self.energy_bar_rect = pygame.Rect((10,34),(ENERGY_BAR_WIDTH,BAR_HEIGHT))

	def display_bar(self,current,max_amount,bg_rect,color):
		# Bg
		pygame.draw.rect(self.screen,UI_BG_COLOR,bg_rect)
		# Calculate stat
		ratio = current / max_amount
		current_width = ratio * bg_rect.width
		current_rect = bg_rect.copy()
		current_rect.width = current_width
		# Bar
		pygame.draw.rect(self.screen,color,current_rect)
		pygame.draw.rect(self.screen,UI_BORDER_COLOR,bg_rect,width=4)

	def display_exp(self,exp):
		text = self.font.render(str(int(exp)),False,TEXT_COLOR)
		text_rect = text.get_rect(bottomright=(WINDOW_WIDTH-20,WINDOW_HEIGHT-20))
		pygame.draw.rect(self.screen,UI_BG_COLOR,text_rect.inflate(20,20))
		self.screen.blit(text,text_rect)
		pygame.draw.rect(self.screen,UI_BORDER_COLOR,text_rect.inflate(20,20),width=4)

	def display_selection_box(self,left,top,has_switched):
		bg_rect = pygame.Rect((left,top),(ITEM_BOX_SIZE,ITEM_BOX_SIZE))
		pygame.draw.rect(self.screen,UI_BG_COLOR,bg_rect)
		if not has_switched:
			pygame.draw.rect(self.screen,UI_BORDER_COLOR_ACTIVE,bg_rect,width=4)
		else:
			pygame.draw.rect(self.screen,UI_BORDER_COLOR,bg_rect,width=4)
		return bg_rect

	def import_images(self,attack_type):
		image_list = [] 
		if attack_type == "weapon":
			data = WEAPON_DATA
		elif attack_type == "magic":
			data = MAGIC_DATA
		for graphic in data.values():
			path = graphic["graphic"]
			image = pygame.image.load(path).convert_alpha()
			image_list.append(image)
		return image_list

	def overlay(self,attack_type,index,has_switched):
		if attack_type == "weapon":
			x = 10
			y = WINDOW_HEIGHT - 90
			image_list = self.import_images("weapon")
		elif attack_type == "magic":
			x = 80
			y = WINDOW_HEIGHT - 85
			image_list = self.import_images("magic")
		bg_rect = self.display_selection_box(x,y,has_switched)
		image = image_list[index]
		rect  = image.get_rect(center=bg_rect.center)
		self.screen.blit(image,rect)

	def display(self,player):
		self.display_bar(player.health,player.stats["health"],self.health_bar_rect,HEALTH_COLOR)
		self.display_bar(player.energy,player.stats["energy"],self.energy_bar_rect,ENERGY_COLOR)
		self.display_exp(player.exp)
		self.overlay("weapon",player.weapon_index,player.can_switch_weapon)
		self.overlay("magic",player.magic_index,player.can_switch_magic)