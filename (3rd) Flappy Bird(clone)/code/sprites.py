<<<<<<< HEAD
import pygame
from settings import *
from random   import choice,randint
class Background(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        bg_image = pygame.image.load("../graphics/environment/background.png").convert()
        bg_image_full_sized = pygame.transform.rotozoom(bg_image,0,SCALE_FACTOR)
        self.image = pygame.Surface((bg_image_full_sized.get_width()*2,bg_image_full_sized.get_height()))
        self.image.blit(bg_image_full_sized,(0,0))
        self.image.blit(bg_image_full_sized,(bg_image_full_sized.get_width(),0))
        self.rect = self.image.get_rect(topleft=(0,0))
        self.pos  = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        self.pos.x -= BACKGROUND_ANIMATION_SPEED*dt
        if self.rect.centerx <= 0: self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.sprite_type = "ground"
        ground_image = pygame.image.load("../graphics/environment/ground.png").convert_alpha()
        self.image = pygame.transform.rotozoom(ground_image,0,SCALE_FACTOR)
        self.rect = self.image.get_rect(bottomleft=(0,WINDOW_HEIGHT))
        self.pos  = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= GROUND_ANIMATION_SPEED*dt
        if self.rect.centerx <= 0: self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.import_images(SCALE_FACTOR)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect  = self.image.get_rect(midleft=(WINDOW_WIDTH//20,WINDOW_HEIGHT/2+10))
        self.pos   = pygame.math.Vector2(self.rect.topleft)
        self.gravity   = GRAVIY
        self.direction = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_sound = pygame.mixer.Sound("../musics/jump.ogg")
        self.jump_sound.set_volume(JUMP_VOLUME)

    def import_images(self,SCALE_FACTOR):
        self.images = []
        for i in range(3):
            image = pygame.image.load(f"../graphics/plane/red_{i}.png").convert_alpha()
            image = pygame.transform.rotozoom(image,0,SCALE_FACTOR/1.7)
            self.images.append(image)

    def apply_gravity(self,dt):
        self.direction += self.gravity*dt
        self.pos.y += self.direction*dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction += JUMP_GRAVITY
        self.jump_sound.play()

    def animate(self,dt):
        self.image_index += PLANE_ANIMATION_SPEED*dt
        if self.image_index >= len(self.images): self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction*PLANE_ROTATION_SPEED,1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.animate(dt)
        self.rotate()
        self.apply_gravity(dt)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.sprite_type = "obstacle"
        orientation = choice(["up","down"])
        image_index = choice([0,1])
        image = pygame.image.load(f"../graphics/obstacle/{image_index}.png").convert_alpha()
        x = WINDOW_WIDTH + randint(50,100)
        if orientation == "up":
            y = WINDOW_HEIGHT + randint(40,80)
            self.image = pygame.transform.rotozoom(image,0,OBSTACLE_SCALE_FACTOR)
            self.rect  = self.image.get_rect(midbottom=(x,y)) 
        else:
            y = randint(-50,-10)
            self.image = pygame.transform.rotozoom(image,180,OBSTACLE_SCALE_FACTOR)
            self.rect  = self.image.get_rect(midtop=(x,y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= OBSTACLE_ANIMATION_SPEED*dt
        self.rect.x = round(self.pos.x)
=======
import pygame
from settings import *
from random   import choice,randint
class Background(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        bg_image = pygame.image.load("../graphics/environment/background.png").convert()
        bg_image_full_sized = pygame.transform.rotozoom(bg_image,0,SCALE_FACTOR)
        self.image = pygame.Surface((bg_image_full_sized.get_width()*2,bg_image_full_sized.get_height()))
        self.image.blit(bg_image_full_sized,(0,0))
        self.image.blit(bg_image_full_sized,(bg_image_full_sized.get_width(),0))
        self.rect = self.image.get_rect(topleft=(0,0))
        self.pos  = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        self.pos.x -= BACKGROUND_ANIMATION_SPEED*dt
        if self.rect.centerx <= 0: self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.sprite_type = "ground"
        ground_image = pygame.image.load("../graphics/environment/ground.png").convert_alpha()
        self.image = pygame.transform.rotozoom(ground_image,0,SCALE_FACTOR)
        self.rect = self.image.get_rect(bottomleft=(0,WINDOW_HEIGHT))
        self.pos  = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= GROUND_ANIMATION_SPEED*dt
        if self.rect.centerx <= 0: self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.import_images(SCALE_FACTOR)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect  = self.image.get_rect(midleft=(WINDOW_WIDTH//20,WINDOW_HEIGHT/2+10))
        self.pos   = pygame.math.Vector2(self.rect.topleft)
        self.gravity   = GRAVIY
        self.direction = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_sound = pygame.mixer.Sound("../musics/jump.ogg")
        self.jump_sound.set_volume(JUMP_VOLUME)

    def import_images(self,SCALE_FACTOR):
        self.images = []
        for i in range(3):
            image = pygame.image.load(f"../graphics/plane/red_{i}.png").convert_alpha()
            image = pygame.transform.rotozoom(image,0,SCALE_FACTOR/1.7)
            self.images.append(image)

    def apply_gravity(self,dt):
        self.direction += self.gravity*dt
        self.pos.y += self.direction*dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction += JUMP_GRAVITY
        self.jump_sound.play()

    def animate(self,dt):
        self.image_index += PLANE_ANIMATION_SPEED*dt
        if self.image_index >= len(self.images): self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction*PLANE_ROTATION_SPEED,1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.animate(dt)
        self.rotate()
        self.apply_gravity(dt)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.sprite_type = "obstacle"
        orientation = choice(["up","down"])
        image_index = choice([0,1])
        image = pygame.image.load(f"../graphics/obstacle/{image_index}.png").convert_alpha()
        x = WINDOW_WIDTH + randint(50,100)
        if orientation == "up":
            y = WINDOW_HEIGHT + randint(40,80)
            self.image = pygame.transform.rotozoom(image,0,OBSTACLE_SCALE_FACTOR)
            self.rect  = self.image.get_rect(midbottom=(x,y)) 
        else:
            y = randint(-50,-10)
            self.image = pygame.transform.rotozoom(image,180,OBSTACLE_SCALE_FACTOR)
            self.rect  = self.image.get_rect(midtop=(x,y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= OBSTACLE_ANIMATION_SPEED*dt
        self.rect.x = round(self.pos.x)
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
        if self.rect.right <= -50: self.kill()