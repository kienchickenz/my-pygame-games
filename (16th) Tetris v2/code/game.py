from settings import *
from random import choice
from timer import Timer

import sys
from os import path

class Game:
	def __init__(self,get_next_shape,update_score):
		# Default
		self.screen = pygame.display.get_surface()
		self.game_surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
		self.game_rect = self.game_surface.get_rect(topleft=(0,0))
		self.all_sprites = pygame.sprite.Group()
		# Shapes
		self.get_next_shape = get_next_shape
		# Grid
		self.grid_surface = self.game_surface.copy()
		self.grid_surface.fill((0,255,0))
		self.grid_surface.set_colorkey((0,255,0))
		self.grid_surface.set_alpha(120)
		# Tetromino
		self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
		self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.all_sprites,self.create_new_tetromino,self.field_data)
		# Timer
		self.down_speed = UPDATE_START_SPEED
		self.down_speed_faster = self.down_speed * 0.2
		self.down_pressed = False
		self.timers = {
			"vertical_move": Timer(self.down_speed,True,self.move_down),
			"horizontal_move": Timer(MOVE_COOLDOWN),
			"rotate": Timer(ROTATE_COOLDOWN)
		}
		self.timers["vertical_move"].activate()
		# Score
		self.current_level = 1
		self.current_score = 0
		self.current_lines = 0
		self.update_score = update_score
		# Music
		self.landing_sound = pygame.mixer.Sound(path.join("..","sound","landing.ogg"))
		self.landing_sound.set_volume(0.1)

	def calculate_score(self,num_lines):
		self.current_lines += num_lines
		self.current_score += SCORE_DATA[num_lines] * self.current_level
		if self.current_lines / 10 > self.current_level: 
			self.current_level += 1
			self.down_speed *= 0.75
			self.down_speed_faster = self.down_speed * 0.2
			self.timers["vertical_move"].duration = self.down_speed
		self.update_score(self.current_lines,self.current_score,self.current_level)

	def check_game_over(self):
		for block in self.tetromino.blocks:
			if block.pos.y < 0: sys.exit()

	def create_new_tetromino(self):
		self.check_game_over()
		self.landing_sound.play()
		self.check_finished_row()
		self.tetromino = Tetromino(
						self.get_next_shape(),
						self.all_sprites,
						self.create_new_tetromino,
						self.field_data)

	def update_timers(self):
		for timer in self.timers.values(): timer.update()

	def move_down(self):
		self.tetromino.move_down()

	def draw_grid(self):
		for col in range(1,COLUMNS):
			x = col * CELL_SIZE
			pygame.draw.line(self.grid_surface,LINE_COLOR,(x,0),(x,self.game_surface.get_height()),LINE_WIDTH)
		for row in range(1,ROWS):
			y = row * CELL_SIZE
			pygame.draw.line(self.grid_surface,LINE_COLOR,(0,y),(self.game_surface.get_width(),y),LINE_WIDTH)
		self.game_surface.blit(self.grid_surface,(0,0))

	def check_finished_row(self):
		delete_rows = []
		for index,row in enumerate(self.field_data):
			if all(row): delete_rows.append(index)
		if delete_rows:
			for delete_row in delete_rows:
				for block in self.field_data[delete_row]:
					block.kill()
				for row in self.field_data:
					for block in row:
						if block and block.pos.y < delete_row: block.pos.y += 1
			# Rebuild field data
			self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
			for block in self.all_sprites:
				self.field_data[int(block.pos.y)][int(block.pos.x)] = block
			# Update score
			self.calculate_score(len(delete_rows))

	def inputs(self):
		keys = pygame.key.get_pressed()
		# Horizontal movement
		if not self.timers["horizontal_move"].active:
			if keys[pygame.K_LEFT]:
				self.tetromino.move_horizontal(-1)
				self.timers["horizontal_move"].activate()
			if keys[pygame.K_RIGHT]:
				self.tetromino.move_horizontal(1)
				self.timers["horizontal_move"].activate()
		# Rotation
		if not self.timers["rotate"].active:
			if keys[pygame.K_UP]:
				self.tetromino.rotate()
				self.timers["rotate"].activate()
		# Speedup
		if not self.down_pressed:
			if keys[pygame.K_DOWN]: 
				self.down_pressed = True
				self.timers["vertical_move"].duration = self.down_speed_faster
		else:
			if not keys[pygame.K_DOWN]:
				self.down_pressed = False
				self.timers["vertical_move"].duration = self.down_speed

	def update(self):
		self.all_sprites.update()
		self.update_timers()

	def draw(self):
		self.game_surface.fill(GRAY)
		self.all_sprites.draw(self.game_surface)
		self.draw_grid()
		pygame.draw.rect(self.game_surface,LINE_COLOR,self.game_rect,2,2)
		
		self.screen.blit(self.game_surface,(PADDING,PADDING))

	def run(self):
		self.inputs()
		self.update()
		self.draw()

class Tetromino:
	def __init__(self,shape,groups,create_new_tetromino,field_data):
		# Setup
		self.shape = shape
		self.block_positions = TETROMINOS[shape]["shape"]
		self.color = TETROMINOS[shape]["color"]
		self.create_new_tetromino = create_new_tetromino
		self.field_data = field_data
		# Blocks
		self.blocks = [Block(groups,pos,self.color) for pos in self.block_positions]

	def next_move_horizontal_collision(self,amount):
		collision_list = [block.horizontal_collision(int(block.pos.x+amount),self.field_data) for block in self.blocks]
		return True if any(collision_list) else False

	def next_move_vertical_collision(self,amount):
		collision_list = [block.vertical_collision(int(block.pos.y+amount),self.field_data) for block in self.blocks]
		return True if any(collision_list) else False

	def move_horizontal(self, amount):
		if not self.next_move_horizontal_collision(amount):
			for block in self.blocks: block.pos.x += amount

	def move_down(self):
		if not self.next_move_vertical_collision(1):
			for block in self.blocks:
				block.pos.y += 1
		else:
			for block in self.blocks:
				self.field_data[int(block.pos.y)][int(block.pos.x)] = block
			self.create_new_tetromino()

	def rotate(self):
		if self.shape != "O":
			pivot_pos = self.blocks[0].pos
			new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
			for pos in new_block_positions:
				# Horizontal check
				if pos.x < 0 or pos.x >= COLUMNS: return
				# Vertical/Floor check 
				if pos.y >= ROWS: return
				# Field check -> collision with other pieces
				if self.field_data[int(pos.y)][int(pos.x)]: return
			for index,block in enumerate(self.blocks):
				block.pos = new_block_positions[index]

class Block(pygame.sprite.Sprite):
	def __init__(self,groups,pos,color):
		super().__init__(groups)
		self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
		self.image.fill(color)
		# Position
		self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
		self.rect = self.image.get_rect(topleft=self.pos*CELL_SIZE)

	def rotate(self,pivot_pos):
		return pivot_pos + (self.pos - pivot_pos).rotate(90)

	def horizontal_collision(self,x,field_data):
		if not 0 <= x <= COLUMNS - 1: return True
		if field_data[int(self.pos.y)][x]: return True

	def vertical_collision(self,y,field_data):
		if not y <= ROWS - 1: return True
		if y >= 0 and field_data[y][int(self.pos.x)]: return True

	def update(self):
		self.rect.topleft = self.pos * CELL_SIZE