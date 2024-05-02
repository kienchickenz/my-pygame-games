import pygame
from settings import *
from support  import *

from pygame.image import load
from pygame.math  import Vector2
from os           import walk

from editor import Editor
from level  import Level

class Main:
	def __init__(self):
		# Defaults
		pygame.mixer.pre_init(44100,-16,2,512)
		pygame.init()
		pygame.display.set_caption("My thirdteen python game")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		# Setup
		self.imports()
		self.editor_active = True
		self.transition = Transition(self.toggle)
		self.editor = Editor(self.land_tiles,self.switch)
		# Cursor
		cursor_image = load("../graphics/cursor/mouse.png").convert_alpha()
		cursor = pygame.cursors.Cursor((0,0),cursor_image)
		pygame.mouse.set_cursor(cursor)

	def imports(self):
		# Terrain
		self.land_tiles = import_folder_dict("../graphics/terrain/land")
		self.water_bottom = load("../graphics/terrain/water/water_bottom.png").convert_alpha()
		self.water_top_animation = import_folder("../graphics/terrain/water/animation")
		# Coin
		self.gold     = import_folder("../graphics/items/gold")
		self.silver   = import_folder("../graphics/items/silver")
		self.diamond  = import_folder("../graphics/items/diamond")
		self.particle = import_folder("../graphics/items/particle")
		# Palm tree
		self.palms = {folder:import_folder(f"../graphics/terrain/palm/{folder}") 
						for folder in list(walk("../graphics/terrain/palm"))[0][1]}
		# Enemies
		self.spikes = load("../graphics/enemies/spikes/spikes.png").convert_alpha()
		self.tooth = {folder:import_folder(f"../graphics/enemies/tooth/{folder}")
						for folder in list(walk("../graphics/enemies/tooth"))[0][1]}
		self.shell = {folder:import_folder(f"../graphics/enemies/shell_left/{folder}")
						for folder in list(walk("../graphics/enemies/shell_left"))[0][1]}
		self.pearl = load("../graphics/enemies/pearl/pearl.png").convert_alpha()
		# Player
		self.player = {folder:import_folder(f"../graphics/player/{folder}")
						for folder in list(walk("../graphics/player"))[0][1]}
		# Clouds
		self.clouds = import_folder("../graphics/clouds")
		# Music
		self.level_music = {
			"coin" :pygame.mixer.Sound("../music/coin.ogg"),
			"hit"  :pygame.mixer.Sound("../music/hit.ogg"),
			"jump" :pygame.mixer.Sound("../music/jump.ogg"),
			"music":pygame.mixer.Sound("../music/superhero.ogg")
		}

	def toggle(self):
		self.editor_active = not self.editor_active
		if self.editor_active:
			self.editor.editor_music.play(loops=-1)

	def switch(self,grid=None):
		self.transition.active = True
		if grid:
			self.level = Level(
							grid,
							self.switch,
							{
							"land" :self.land_tiles,
							"water bottom":self.water_bottom,
							"water top"   :self.water_top_animation,
							"gold"    :self.gold,
							"silver"  :self.silver,
							"diamond" :self.diamond,
							"particle":self.particle,
							"palms":self.palms,
							"spikes":self.spikes,
							"tooth" :self.tooth,
							"shell" :self.shell,
							"pearl" :self.pearl,
							"player":self.player,
							"cloud" :self.clouds
							},
							self.level_music
							)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000

			if self.editor_active:
				self.editor.run(dt)
			else:
				self.level.run(dt)
			self.transition.display(dt)
			pygame.display.update()

class Transition:
	def __init__(self,toggle):
		self.screen = pygame.display.get_surface()
		self.toggle = toggle
		self.active = False

		self.border_width = 0
		self.direction = 1
		self.center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
		self.radius = Vector2(self.center).magnitude()
		self.threshold = self.radius + 50

	def display(self,dt):
		if self.active:
			self.border_width += 1000 * dt * self.direction
			if self.border_width >= self.threshold:
				self.direction = -1
				self.toggle()
			if self.border_width < 0:
				self.active = False
				self.border_width = 0
				self.direction = 1
			pygame.draw.circle(self.screen,"black",self.center,self.radius,int(self.border_width))

if __name__ == "__main__":
	main = Main()
	main.run()