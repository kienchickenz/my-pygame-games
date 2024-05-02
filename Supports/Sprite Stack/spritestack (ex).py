import sys
import os
import math

import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)
display = pygame.Surface((100, 100))

images = [pygame.image.load('car/' + img) for img in os.listdir('car')]

clock = pygame.time.Clock()

def render_stack(surf, images, pos, rotation, spread=1):
    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))
        
frame = 0

while True:
    display.fill((0, 0, 0))
    
    frame += 1
    
    render_stack(display, images, (50, 50), frame)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)
    
