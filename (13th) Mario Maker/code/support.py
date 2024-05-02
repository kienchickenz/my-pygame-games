import pygame
from os import walk

def import_folder(path):
	image_list = []
	for _,_,file_names in walk(path):
		for file_name in file_names:
			image = pygame.image.load(f"{path}/{file_name}").convert_alpha()
			image_list.append(image)
	return image_list

def import_folder_dict(path):
	image_dict = {}
	for _,_,file_names in walk(path): 
		for file_name in file_names:
			image = pygame.image.load(f"{path}/{file_name}").convert_alpha()
			image_dict[file_name.split(".")[0]] = image
	return image_dict