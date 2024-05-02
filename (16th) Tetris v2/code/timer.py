import pygame

class Timer:
	def __init__(self,duration,repeated=False,func=None):
		self.duration = duration
		self.repeated = repeated
		self.func = func
		self.start_time = 0
		self.active = False

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False

	def update(self):
		current_time = pygame.time.get_ticks()
		if self.active:
			if current_time - self.start_time >= self.duration:
				if self.func: self.func()
				if self.repeated: self.activate()
				else: self.deactivate()