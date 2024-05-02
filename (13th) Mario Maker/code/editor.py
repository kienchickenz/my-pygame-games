import pygame,sys
from pygame.math import Vector2
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load
from random       import choice,randint

from settings import *
from menu     import Menu
from support  import *
from timer    import Timer

class Editor:
	def __init__(self,land_tiles,switch):
		self.screen = pygame.display.get_surface()
		self.switch = switch
		self.canvas_data = {}
		# Imports
		self.land_tiles = land_tiles
		self.water_bottom = None
		self.animations = {}
		self.preview_images = {}
		self.imports()
		# Navigation
		self.origin = Vector2()
		self.pan_active = False
		self.pan_offset = Vector2()
		# Support lines
		self.support_line_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.support_line_surf.set_colorkey("green")
		self.support_line_surf.set_alpha(30)
		# Selection
		self.selection_index = 2
		self.last_selected_cell = None
		# Menu
		self.menu = Menu()
		# Objects
		self.canvas_objects = pygame.sprite.Group()
		self.foreground     = pygame.sprite.Group()
		self.background     = pygame.sprite.Group()
		self.object_drag_active = False
		self.object_timer = Timer(400)
		self.player = CanvasObject(
			groups=[self.canvas_objects,self.foreground],
			pos=(200,WINDOW_HEIGHT/2),
			images=self.animations[0]["images"],
			tile_id=0,
			origin=self.origin
			)
		self.sky_handle = CanvasObject(
			groups=[self.canvas_objects,self.background],
			pos=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),
			images=[self.sky_handle_image],
			tile_id=1,
			origin=self.origin
			)
		# Clouds
		self.current_clouds = []
		self.cloud_images = import_folder("../graphics/clouds")
		self.cloud_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.cloud_timer,2000)
		self.startup_clouds()
		# Music
		self.editor_music = pygame.mixer.Sound("../music/explorer.ogg")
		self.editor_music.set_volume(0.4)
		self.editor_music.play(loops=-1)

	# Support
	def get_current_cell(self,obj=None):
		if not obj:
			distance_to_origin = Vector2(mouse_pos()) - self.origin
		else:
			distance_to_origin = Vector2(obj.distance_to_origin) - self.origin
		if distance_to_origin.x > 0:
			col = int(distance_to_origin.x / TILE_SIZE)
		else:
			col = int(distance_to_origin.x / TILE_SIZE) - 1
		if distance_to_origin.y > 0:
			row = int(distance_to_origin.y / TILE_SIZE)
		else:
			row = int(distance_to_origin.y / TILE_SIZE) - 1
		return col,row

	def check_neighbors(self,cell_pos):
		cluster_size = 3
		local_cluster = [
			(cell_pos[0] + col - int(cluster_size/2),cell_pos[1] + row - int(cluster_size/2))
			for col in range(cluster_size) 
			for row in range(cluster_size)
						]
		for cell in local_cluster:
			if cell in self.canvas_data:
				self.canvas_data[cell].terrain_neighbors = []
				self.canvas_data[cell].water_on_top = False
				for name,side in NEIGHBOR_DIRECTIONS.items():
					neighbor_cell = (cell[0] + side[0],cell[1] + side[1])
					if neighbor_cell in self.canvas_data:
						# Water top neighbor
						if self.canvas_data[neighbor_cell].has_water and name == "A":
							self.canvas_data[cell].water_on_top = True
						# Terrain neighbors
						if self.canvas_data[neighbor_cell].has_terrain:
							self.canvas_data[cell].terrain_neighbors.append(name)

	def imports(self):
		self.water_bottom = load("../graphics/terrain/water/water_bottom.png").convert()
		self.sky_handle_image = load("../graphics/cursor/handle.png").convert_alpha()
		# Animation
		for key,value in EDITOR_DATA.items():
			if value["graphics"]:
				images = import_folder(value["graphics"])
				self.animations[key] = {
					"image index":0,
					"images":images,
					"length":len(images)
										}
		# Preview
		self.preview_images = {key:load(value["preview"]).convert_alpha() for key,value in EDITOR_DATA.items() if value["preview"]}

	def animation_update(self,dt):
		for value in self.animations.values():
			value["image index"] += ANIMATION_SPEED*dt
			if value["image index"] >= value["length"]:
				value["image index"] = 0

	def mouse_on_object(self):
		for sprite in self.canvas_objects:
			if sprite.rect.collidepoint(mouse_pos()):
				return sprite

	def create_grid(self):
		# Add object to tiles
		for tile in self.canvas_data.values():
			tile.objects = []
		for obj in self.canvas_objects:
			current_cell = self.get_current_cell(obj)
			offset = Vector2(obj.distance_to_origin) - Vector2(current_cell)*TILE_SIZE
			if current_cell in self.canvas_data:
				self.canvas_data[current_cell].add_id(obj.tile_id,offset)
			else:
				self.canvas_data[current_cell] = CanvasTile(obj.tile_id,offset)
		# Create an empty grid
		layers = {
			"water"     :{},
			"bg palms"  :{},
			"terrain"   :{},
			"enemies"   :{},
			"coins"     :{},
			"fg objects":{},
		}
		# Grid offset
		left = sorted(self.canvas_data.keys(),key=lambda tile:tile[0])[0][0]
		top  = sorted(self.canvas_data.keys(),key=lambda tile:tile[1])[0][1]
		# Fill the grid
		for tile_pos,tile in self.canvas_data.items():
			col_adjusted = tile_pos[0] - left
			row_adjusted = tile_pos[1] - top
			x = col_adjusted * TILE_SIZE
			y = row_adjusted * TILE_SIZE
			if tile.has_water:
				layers["water"][(x,y)] = tile.get_water()
			if tile.has_terrain:
				layers["terrain"][(x,y)] = tile.get_terrain() if tile.get_terrain() in self.land_tiles else "X"
			if tile.coin:
				layers["coins"][(x + TILE_SIZE//2,y + TILE_SIZE//2)] = tile.coin
			if tile.enemy:
				layers["enemies"][(x,y)] = tile.enemy
			if tile.objects:
				for obj,offset in tile.objects:
					if obj in [key for key,value in EDITOR_DATA.items() if value["style"] == "palm_bg"]:
						layers["bg palms"][(int(x + offset.x),int(y + offset.y))] = obj
					else:
						layers["fg objects"][(int(x + offset.x),int(y + offset.y))] = obj

		return layers

	# Input
	def event_loop(self):
		for event in pygame.event.get():
			if event.type==pygame.QUIT                             : sys.exit()
			if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
			if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
				self.switch(self.create_grid())
				self.editor_music.stop()
			self.pan_input(event)
			self.selection_hotkeys(event)
			self.menu_click(event)
			
			self.object_drag(event)
			
			self.canvas_add()
			self.canvas_remove()

			self.create_clouds(event)
			
	def pan_input(self,event):
		# Middle mouse
		if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
			self.pan_active = True
			self.pan_offset = Vector2(mouse_pos()) - self.origin
		if not mouse_buttons()[1]:
			self.pan_active = False
		# Mouse wheel
		if event.type == pygame.MOUSEWHEEL:
			if pygame.key.get_pressed()[pygame.K_LCTRL]:
				self.origin.y -= event.y * 50
			else:
				self.origin.x -= event.y * 50
			for sprite in self.canvas_objects:
				sprite.pan_pos(self.origin)
		# Panning update
		if self.pan_active:
			self.origin = Vector2(mouse_pos()) - self.pan_offset
			for sprite in self.canvas_objects:
				sprite.pan_pos(self.origin)

	def menu_click(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.menu.rect.collidepoint(mouse_pos()):
				new_index = self.menu.click(mouse_pos(),mouse_buttons())
				self.selection_index = new_index if new_index else self.selection_index

	def selection_hotkeys(self,event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				self.selection_index += 1
			if event.key == pygame.K_LEFT:
				self.selection_index -= 1
			self.selection_index = max(min(self.selection_index,18),2)

	def canvas_add(self):
		if mouse_buttons()[0] and not self.object_drag_active: 
			if not self.menu.rect.collidepoint(mouse_pos()):
				current_cell = self.get_current_cell()
				# Tile
				if EDITOR_DATA[self.selection_index]["type"] == "tile":
					if current_cell != self.last_selected_cell:
						if current_cell in self.canvas_data:
							self.canvas_data[current_cell].add_id(self.selection_index)
						else:
							self.canvas_data[current_cell] = CanvasTile(self.selection_index)
						self.check_neighbors(current_cell)
						self.last_selected_cell = current_cell
				# Object
				else:
					if not self.object_timer.active:
						if EDITOR_DATA[self.selection_index]["style"] == "palm_bg":
							groups = [self.canvas_objects,self.background] 
						else: 
							groups = [self.canvas_objects,self.foreground]
						CanvasObject(
							groups=groups,
							pos=mouse_pos(),
							images=self.animations[self.selection_index]["images"],
							tile_id=self.selection_index,
							origin=self.origin
							)
						self.object_timer.activate()

	def canvas_remove(self):
		if mouse_buttons()[2]:
			# Tile
			if not self.menu.rect.collidepoint(mouse_pos()):
				if self.canvas_data:
					current_cell = self.get_current_cell()
					if current_cell in self.canvas_data:
						self.canvas_data[current_cell].remove_id(self.selection_index)
						if self.canvas_data[current_cell].is_empty:
							del self.canvas_data[current_cell]
						self.check_neighbors(current_cell)
			# Object
			selected_object = self.mouse_on_object()
			if selected_object:
				if EDITOR_DATA[selected_object.tile_id]["style"] not in ("sky","player"): 
					selected_object.kill()

	def object_drag(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if mouse_buttons()[0]:
				for sprite in self.canvas_objects:
					if sprite.rect.collidepoint(mouse_pos()):
						sprite.start_drag()
						self.object_drag_active = True
		if event.type == pygame.MOUSEBUTTONUP: 
			if self.object_drag_active:
				for sprite in self.canvas_objects:
					if sprite.selected:
						sprite.drag_end(self.origin)
						self.object_drag_active = False

	# Draw
	def draw_tile_lines(self):
		cols = WINDOW_WIDTH // TILE_SIZE
		rows = WINDOW_HEIGHT // TILE_SIZE
		origin_offset = Vector2(
					x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
					y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
						)
		self.support_line_surf.fill("green")
		for col in range(cols + 1):
			x = origin_offset.x + col*TILE_SIZE
			pygame.draw.line(self.support_line_surf,LINE_COLOR,(x,0),(x,WINDOW_HEIGHT))
		for row in range(rows + 1):
			y = origin_offset.y + row*TILE_SIZE
			pygame.draw.line(self.support_line_surf,LINE_COLOR,(0,y),(WINDOW_WIDTH,y))
		self.screen.blit(self.support_line_surf,(0,0))

	def draw_level(self):
		self.background.draw(self.screen)
		for cell_pos,tile in self.canvas_data.items():
			pos = self.origin + Vector2(cell_pos) * TILE_SIZE
			# Water
			if tile.has_water:
				if tile.water_on_top:
					self.screen.blit(self.water_bottom,pos)
				else:
					images = self.animations[3]["images"]
					image_index = int(self.animations[3]["image index"])
					image = images[image_index]
					self.screen.blit(image,pos)
			# Terrain
			if tile.has_terrain:
				terrain_string = "".join(tile.terrain_neighbors)
				terrain_style = terrain_string if terrain_string in self.land_tiles else "X"
				self.screen.blit(self.land_tiles[terrain_style],pos)
			# Coin
			if tile.coin:
				images = self.animations[tile.coin]["images"]
				image_index = int(self.animations[tile.coin]["image index"])
				image = images[image_index]
				rect = image.get_rect(center=(pos[0] + TILE_SIZE/2,pos[1] + TILE_SIZE/2))
				self.screen.blit(image,rect)
			# Enemy
			if tile.enemy:
				images = self.animations[tile.enemy]["images"]
				image_index = int(self.animations[tile.enemy]["image index"])
				image = images[image_index]
				rect = image.get_rect(midbottom=(pos[0] + TILE_SIZE/2,pos[1] + TILE_SIZE))
				self.screen.blit(image,rect)
		self.foreground.draw(self.screen)

	def draw_preview(self):
		selected_object = self.mouse_on_object()
		if not self.menu.rect.collidepoint(mouse_pos()):
			if selected_object:
				# Indicator
				rect = selected_object.rect.inflate(10,10)
				color = "black"
				width = 3
				size = 15
				# Topleft
				pygame.draw.lines(self.screen,color,False,((rect.left,rect.top+size),rect.topleft,(rect.left+size,rect.top)),width)
				# Topright
				pygame.draw.lines(self.screen,color,False,((rect.right,rect.top+size),rect.topright,(rect.right-size,rect.top)),width)
				# Bottomleft
				pygame.draw.lines(self.screen,color,False,((rect.left,rect.bottom-size),rect.bottomleft,(rect.left+size,rect.bottom)),width)
				# Bottomright
				pygame.draw.lines(self.screen,color,False,((rect.right,rect.bottom-size),rect.bottomright,(rect.right-size,rect.bottom)),width)
			else:
				# Preview
				type_dict = {key:value["type"] for key,value in EDITOR_DATA.items()}
				image = self.preview_images[self.selection_index].copy()
				image.set_alpha(200)
				# Tile
				if type_dict[self.selection_index] == "tile":
					current_cell = self.get_current_cell()
					rect = image.get_rect(topleft=self.origin+Vector2(current_cell)*TILE_SIZE)
				# Object
				else:
					rect = image.get_rect(center=mouse_pos())
				self.screen.blit(image,rect)

	def draw_sky(self,dt):
		self.screen.fill(SKY_COLOR)
		y = self.sky_handle.rect.centery
		# Horizon lines
		horizon_rect_1 = pygame.Rect((0,y-10),(WINDOW_WIDTH,10))
		horizon_rect_2 = pygame.Rect((0,y-16),(WINDOW_WIDTH,4))
		horizon_rect_3 = pygame.Rect((0,y-20),(WINDOW_WIDTH,2))
		pygame.draw.rect(self.screen,HORIZON_TOP_COLOR,horizon_rect_1)
		pygame.draw.rect(self.screen,HORIZON_TOP_COLOR,horizon_rect_2)
		pygame.draw.rect(self.screen,HORIZON_TOP_COLOR,horizon_rect_3)
		self.draw_clouds(dt,y)
		# Sea
		sea_rect = pygame.Rect((0,y),(WINDOW_WIDTH,WINDOW_HEIGHT-y))
		pygame.draw.rect(self.screen,SEA_COLOR,sea_rect)
		pygame.draw.line(self.screen,HORIZON_COLOR,(0,y),(WINDOW_WIDTH,y),3)

	def draw_clouds(self,dt,horizon_y):
		if horizon_y > 0:
			for cloud in self.current_clouds:
				cloud["pos"][0] -= cloud["speed"]*dt
				x = cloud["pos"][0]
				y = horizon_y - cloud["pos"][1]
				self.screen.blit(cloud["image"],(x,y))

	def create_clouds(self,event):
		if event.type == self.cloud_timer:
			image = choice(self.cloud_images) 
			image = pygame.transform.scale2x(image) if randint(0,4) < 2 else image
			pos = [WINDOW_WIDTH + randint(50,100),randint(0,WINDOW_HEIGHT)]
			self.current_clouds.append({"image":image,"pos":pos,"speed":randint(20,50)})
			self.current_clouds = [cloud for cloud in self.current_clouds if cloud["pos"][0] > -600]

	def startup_clouds(self):
		for i in range(20):
			image = pygame.transform.scale2x(choice(self.cloud_images)) if randint(0,4) < 2 else choice(self.cloud_images)
			pos = [randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)]
			self.current_clouds.append({"image":image,"pos":pos,"speed":randint(20,50)})

	# Update
	def run(self,dt):
		self.event_loop()
		# Update
		self.animation_update(dt)
		self.canvas_objects.update(dt)
		self.object_timer.update()
		# Draw
		self.screen.fill("grey")
		self.draw_sky(dt)
		self.draw_level()
		self.draw_tile_lines()
		# pygame.draw.circle(self.screen,"orange",self.origin,30)
		self.draw_preview()
		self.menu.display(self.selection_index)

class CanvasTile:
	def __init__(self,tile_id,offset=Vector2()):
		# Terrain
		self.has_terrain = False
		self.terrain_neighbors = []
		# Water
		self.has_water = False
		self.water_on_top = False
		# Coin
		self.coin = None
		# Enemy
		self.enemy = None
		# Objects
		self.objects = []
		self.add_id(tile_id,offset=offset)
		self.is_empty = False

	def add_id(self,tile_id,offset=Vector2()):
		options = {key:value["style"] for key,value in EDITOR_DATA.items()}
		match options[tile_id]:
			case "terrain": self.has_terrain = True
			case "water"  : self.has_water = True
			case "coin"   : self.coin = tile_id
			case "enemy"  : self.enemy = tile_id
			case _        : 
				if (tile_id,offset) not in self.objects:
					self.objects.append((tile_id,offset))

	def remove_id(self,tile_id):
		options = {key:value["style"] for key,value in EDITOR_DATA.items()}
		match options[tile_id]:
			case "terrain": self.has_terrain = False
			case "water"  :	self.has_water = False
			case "coin"   :	self.coin = None
			case "enemy"  :	self.enemy = None
		self.check_content()

	def check_content(self):
		if not self.has_terrain and not self.has_water and not self.coin and not self.enemy:
			self.is_empty = True

	def get_water(self):
		return "bottom" if self.water_on_top else "top"

	def get_terrain(self):
		return "".join(self.terrain_neighbors)

class CanvasObject(pygame.sprite.Sprite):
	def __init__(self,groups,pos,images,tile_id,origin):
		super().__init__(groups)
		self.tile_id = tile_id
		# Animation
		self.images = images
		self.image_index = 0
		self.image = self.images[self.image_index]
		self.rect = self.image.get_rect(center=pos)
		# Move
		self.distance_to_origin = Vector2(self.rect.topleft) - origin
		self.selected = False
		self.mouse_offset = Vector2()

	def start_drag(self):
		self.selected = True
		self.mouse_offset = Vector2(mouse_pos()) - Vector2(self.rect.topleft)

	def drag(self):
		if self.selected:
			self.rect.topleft = Vector2(mouse_pos()) - self.mouse_offset

	def drag_end(self,origin):
		self.selected = False
		self.distance_to_origin = Vector2(self.rect.topleft) - origin

	def animate(self,dt):
		self.image_index += ANIMATION_SPEED*dt
		if self.image_index >= len(self.images): self.image_index = 0
		self.image = self.images[int(self.image_index)]
		self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

	def pan_pos(self,origin):
		self.rect.topleft = origin + self.distance_to_origin

	def update(self,dt):
		self.animate(dt)
		self.drag()