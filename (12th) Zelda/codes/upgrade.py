import pygame
from settings import *
from pygame.math import Vector2

class Upgrade:
	def __init__(self,player):
		self.screen = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
		self.player = player
		self.attribute_number = len(player.stats)
		self.attribute_names = list(player.stats.keys())
		self.max_values = list(player.max_stats.values())
		# Selection system
		self.selection_index = 0
		self.select_time = 0
		self.can_select = True
		self.select_cooldown = 200
		self.move_time = 0
		self.can_move = True
		self.move_cooldown = 300
		# Item dimensions
		self.item_list = []
		self.width  = WINDOW_WIDTH // (self.attribute_number + 1)
		self.height = WINDOW_HEIGHT * 0.8
		self.create_items()

	def input(self):
		keys = pygame.key.get_pressed()
		if self.can_move:
			if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
				self.selection_index += 1
				self.can_move = False
				self.move_time = pygame.time.get_ticks()
			elif keys[pygame.K_LEFT] and self.selection_index > 0:
				self.selection_index -= 1
				self.can_move = False
				self.move_time = pygame.time.get_ticks()
		if self.can_select:
			if keys[pygame.K_SPACE]:
				self.can_select = False
				self.select_time = pygame.time.get_ticks()
				self.item_list[self.selection_index].trigger(self.player)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_move:
			if current_time - self.move_time > self.move_cooldown:
				self.can_move = True
		if not self.can_select:
			if current_time - self.select_time > self.select_cooldown:
				self.can_select = True

	def create_items(self):
		for index in range(self.attribute_number):
			left = self.width * index + self.width/6 * (index + 1)
			top = (WINDOW_HEIGHT - self.height)/2
			item = Item(left,top,self.width,self.height,index,self.font)
			self.item_list.append(item)

	def update(self):
		self.input()
		self.cooldowns()
		for index,item in enumerate(self.item_list):
			name = self.attribute_names[index]
			value = list(self.player.stats.values())[index]
			max_value = self.max_values[index]
			cost = list(self.player.upgrade_cost.values())[index]
			item.display(self.screen,self.selection_index,name,value,max_value,cost)

class Item:
	def __init__(self,left,top,width,height,index,font):
		self.rect = pygame.Rect((left,top),(width,height))
		self.index = index
		self.font = font

	def display_names(self,surface,name,cost,selected):
		color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
		title = self.font.render(name,False,color)
		title_offset = Vector2(0,20)
		title_rect = title.get_rect(midtop=self.rect.midtop+title_offset)
		cost = self.font.render(f"{int(cost)}",False,color)
		cost_offset = Vector2(0,-20)
		cost_rect = cost.get_rect(midbottom=self.rect.midbottom+cost_offset)
		surface.blit(title,title_rect)
		surface.blit(cost,cost_rect)

	def display_bar(self,surface,value,max_value,selected):
		offset = Vector2(0,60)
		top = self.rect.midtop + offset
		bottom = self.rect.midbottom - offset
		color = BAR_COLOR_SELECTED if selected else BAR_COLOR
		full_height = bottom[1] - top[1]
		relative_number = (value/max_value) * full_height
		value_rect = pygame.Rect((bottom[0]-30/2,bottom[1]-relative_number),(30,10))
		pygame.draw.line(surface,color,top,bottom,5)
		pygame.draw.rect(surface,color,value_rect)

	def trigger(self,player):
		upgrade_attribute = list(player.stats.keys())[self.index]
		if player.exp >= player.upgrade_cost[upgrade_attribute]:
			if player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
				player.exp -= player.upgrade_cost[upgrade_attribute]
				player.stats[upgrade_attribute] *= 1.2
				player.upgrade_cost[upgrade_attribute] *= 1.4
		if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
			player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

	def display(self,surface,selected_number,name,value,max_value,cost):
		if self.index == selected_number:
			pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
			pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
		else:
			pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
			pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
		self.display_names(surface,name,cost,self.index==selected_number)
		self.display_bar(surface,value,max_value,self.index==selected_number)