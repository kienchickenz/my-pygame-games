<<<<<<< HEAD
import pygame

pygame.init()
font = pygame.font.Font(None,30)
def debug(info,y=10,x=10):
    screen = pygame.display.get_surface()
    debug  = font.render(str(info),True,"white")
    debug_rect = debug.get_rect(topleft=(x,y))
    pygame.draw(screen,"black",debug_rect)
=======
import pygame

pygame.init()
font = pygame.font.Font(None,30)
def debug(info,y=10,x=10):
    screen = pygame.display.get_surface()
    debug  = font.render(str(info),True,"white")
    debug_rect = debug.get_rect(topleft=(x,y))
    pygame.draw(screen,"black",debug_rect)
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
    screen.blit(debug,debug_rect)