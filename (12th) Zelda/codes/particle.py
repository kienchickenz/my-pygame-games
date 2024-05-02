import pygame
from os import walk
from random import choice

class AnimationPlayer:
	def __init__(self):
		self.animations = {
			# magic
			'flame': self.import_folder('../graphics/particles/flame/frames'),
			'aura' : self.import_folder('../graphics/particles/aura'),
			'heal' : self.import_folder('../graphics/particles/heal/frames'),
			
			# attacks 
			'claw'       : self.import_folder('../graphics/particles/claw'),
			'slash'      : self.import_folder('../graphics/particles/slash'),
			'sparkle'    : self.import_folder('../graphics/particles/sparkle'),
			'leaf_attack': self.import_folder('../graphics/particles/leaf_attack'),
			'thunder'    : self.import_folder('../graphics/particles/thunder'),

			# monster deaths
			'squid'  : self.import_folder('../graphics/particles/smoke_orange'),
			'raccoon': self.import_folder('../graphics/particles/raccoon'),
			'spirit' : self.import_folder('../graphics/particles/nova'),
			'bamboo' : self.import_folder('../graphics/particles/bamboo'),
			
			# leafs 
			'leaf': (
				self.import_folder('../graphics/particles/leaf1'),
				self.import_folder('../graphics/particles/leaf2'),
				self.import_folder('../graphics/particles/leaf3'),
				self.import_folder('../graphics/particles/leaf4'),
				self.import_folder('../graphics/particles/leaf5'),
				self.import_folder('../graphics/particles/leaf6'),
				self.reflect_images(self.import_folder('../graphics/particles/leaf1')),
				self.reflect_images(self.import_folder('../graphics/particles/leaf2')),
				self.reflect_images(self.import_folder('../graphics/particles/leaf3')),
				self.reflect_images(self.import_folder('../graphics/particles/leaf4')),
				self.reflect_images(self.import_folder('../graphics/particles/leaf5')),
				self.reflect_images(self.import_folder('../graphics/particles/leaf6'))
				)
			}

	def import_folder(self,path):
		image_list = []
		for _,_,images in walk(path):
			for image in images:
				full_path = path + "/" + image
				image = pygame.image.load(full_path).convert_alpha()
				image_list.append(image)
		return image_list

	def reflect_images(self,image_list):
		new_image_list = []
		for image in image_list:
			flipped_image = pygame.transform.flip(image,flip_x=True,flip_y=False)
			new_image_list.append(flipped_image)
		return new_image_list

	def create_grass_particles(self,groups,pos):
		image_list = choice(self.animations["leaf"])
		ParticleEffect(groups,pos,image_list)

	def create_particles(self,groups,pos,particle_type):
		image_list = self.animations[particle_type]
		ParticleEffect(groups,pos,image_list)

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,groups,pos,image_list):
		super().__init__(groups)
		self.sprite_type = "magic"
		self.image_index = 0
		self.animation_speed = 8
		self.image_list = image_list
		self.image = self.image_list[self.image_index]
		self.rect  = self.image.get_rect(center=pos)

	def animate(self,dt):
		self.image_index += self.animation_speed*dt
		if self.image_index >= len(self.image_list):
			self.kill()
		else:
			self.image = self.image_list[int(self.image_index)]

	def update(self,dt):
		self.animate(dt)