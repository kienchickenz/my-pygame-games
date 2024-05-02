import pygame
from os import walk

def import_folder(path):
	image_list = []
	for _,_,image_files in walk(path):
		for image_name in image_files:
			full_path = path + f"/{image_name}"
			image = pygame.image.load(full_path).convert_alpha()
			image_list.append(image)
	return image_list

def import_folder_dict(path):
	image_dict = {}
	for _,_,image_files in walk(path):
		for image_name in image_files:
			full_path = path + f"/{image_name}"
			image = pygame.image.load(full_path).convert_alpha()
			key = image_name.split(".")[0]
			image_dict[key] = image
	return image_dict