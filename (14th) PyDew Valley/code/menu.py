import pygame
from settings import *
from timer    import Timer

class Menu:
	def __init__(self,player,toggle_menu):
		self.screen = pygame.display.get_surface()
		self.font = pygame.font.Font("../font/LycheeSoda.ttf",30)
		self.buy_text  = self.font.render("buy",False,"black") 
		self.sell_text = self.font.render("sell",False,"black")
		self.player = player
		self.toggle_menu = toggle_menu
		# Menu rect
		self.menu_width  = 400
		self.menu_height = 0
		self.space = 10
		self.padding = 8
		# Entries
		self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
		self.sell_border = len(self.player.item_inventory) - 1
		self.texts = []
		self.setup()
		# Selection
		self.selection_index = 0
		self.timer = Timer(200)

	def setup(self):
		for item in self.options:
			text = self.font.render(item,False,"black")
			self.texts.append(text)
			self.menu_height += self.padding + text.get_height() + self.padding
		self.menu_height += (len(self.texts) - 1) * self.space
		self.menu_top  = WINDOW_HEIGHT / 2 - self.menu_height / 2
		self.menu_left = WINDOW_WIDTH / 2 - self.menu_width / 2
		self.menu_rect = pygame.Rect((self.menu_left,self.menu_top),(self.menu_width,self.menu_height))

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			self.toggle_menu()
		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.selection_index -= 1
				self.timer.activate()
			if keys[pygame.K_DOWN]:
				self.selection_index += 1
				self.timer.activate()
			if self.selection_index < 0: self.selection_index = len(self.options) - 1
			if self.selection_index > len(self.options) - 1: self.selection_index = 0
			if keys[pygame.K_SPACE]:
				self.timer.activate()
				current_item = self.options[self.selection_index]
				if self.selection_index <= self.sell_border: # Sell
					if self.player.item_inventory[current_item] > 0:
						self.player.item_inventory[current_item] -= 1
						self.player.money += SALE_PRICES[current_item]
				else:# Buy
					seed_price = PURCHASE_PRICES[current_item]
					if self.player.money >= seed_price:
						self.player.seed_inventory[current_item] += 1
						self.player.money -= seed_price

	def display_money(self):
		text = self.font.render(f"${self.player.money}",False,"black")
		text_rect = text.get_rect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT-20))
		pygame.draw.rect(self.screen,"white",text_rect.inflate(10,10),0,4)
		self.screen.blit(text,text_rect) 

	def display_entry(self,text,amount,top,selected):
		# Background
		bg_rect = pygame.Rect((self.menu_rect.left,top),(self.menu_width,text.get_height() + self.padding * 2))
		pygame.draw.rect(self.screen,"white",bg_rect,0,4)
		# Text
		text_rect = text.get_rect(midleft=(self.menu_rect.left+20,bg_rect.centery))
		self.screen.blit(text,text_rect)
		# Amount
		amount = self.font.render(str(amount),False,"black")
		amount_rect = amount.get_rect(midright=(self.menu_rect.right-20,bg_rect.centery))
		self.screen.blit(amount,amount_rect)
		# Selected
		if selected:
			pygame.draw.rect(self.screen,"black",bg_rect,4,4)
			if self.selection_index <= self.sell_border: # Sell
				pos = self.sell_text.get_rect(midleft=(self.menu_rect.left + 150,bg_rect.centery))
				self.screen.blit(self.sell_text,pos)
			else: # Buy
				pos = self.buy_text.get_rect(midleft=(self.menu_rect.left + 150,bg_rect.centery))
				self.screen.blit(self.buy_text,pos)

	def update(self):
		self.input()
		self.timer.update()
		self.display_money()
		for index,text in enumerate(self.texts):
			top = self.menu_rect.top + index * (text.get_height() + self.padding*2 + self.space)
			amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
			self.display_entry(text,amount_list[index],top,self.selection_index==index)