<<<<<<< HEAD
import pygame,sys,time
from settings import *
from sprites  import Background,Ground,Plane,Obstacle

class Game:
    def __init__(self):
        # Defaults
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.init()
        pygame.display.set_caption("My third python game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        # Setup
        Background(self.all_sprites)
        Ground([self.all_sprites,self.collision_sprites])
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,OBSTACLE_SPAWNING_SPEED)
        self.end_game = True
        # Score setup
        self.font = pygame.font.Font("../fonts/BD_Cartoon_Shout.ttf",FONT_SIZE)
        self.score_text = 0
        self.start_offset = 0
        # Menu setup
        menu      = pygame.image.load("../graphics/ui/menu.png").convert_alpha()
        self.menu = pygame.transform.rotozoom(menu,0,SCALE_FACTOR)
        self.menu_rect = self.menu.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        # Music 
        self.bg_music  = pygame.mixer.Sound("../musics/music.ogg")
        self.bg_music.play(loops=-1)

    def detect_collision(self):
        if self.plane.rect.top <= 0: self.do_end_game()
        if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False):
            if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask):
                self.do_end_game()

    def do_end_game(self):
        self.end_game = True
        self.plane.kill()
        for sprite in self.collision_sprites: 
            if sprite.sprite_type == "obstacle": sprite.kill()

    def draw_score(self):
        if not self.end_game: 
            self.score_text = (pygame.time.get_ticks()-self.start_offset)//1000
            score_y = WINDOW_HEIGHT/10
        else:
            score_y = WINDOW_HEIGHT/2 + self.menu_rect.height/1.5
        score      = self.font.render(f"{self.score_text}",True,SCORE_COLOR)
        score_rect = score.get_rect(midtop=(WINDOW_WIDTH/2,score_y))
        self.screen.blit(score,score_rect)

    def restart(self):
        self.end_game = False
        self.plane = Plane(self.all_sprites)
        self.start_offset = pygame.time.get_ticks()

    def run(self):
        prev_time = time.time()
        while True:
            dt        = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT                               : sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if not self.end_game: self.plane.jump()
                    else: self.restart()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not self.end_game: self.plane.jump()
                    else: self.restart()
                if event.type == self.obstacle_timer and not self.end_game:
                    Obstacle([self.all_sprites,self.collision_sprites])
            self.screen.fill(BACKGROUND_COLOR)
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.draw_score()
            if not self.end_game: 
                self.detect_collision()
            else:
                self.screen.blit(self.menu,self.menu_rect)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
=======
import pygame,sys,time
from settings import *
from sprites  import Background,Ground,Plane,Obstacle

class Game:
    def __init__(self):
        # Defaults
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.init()
        pygame.display.set_caption("My third python game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        # Setup
        Background(self.all_sprites)
        Ground([self.all_sprites,self.collision_sprites])
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,OBSTACLE_SPAWNING_SPEED)
        self.end_game = True
        # Score setup
        self.font = pygame.font.Font("../fonts/BD_Cartoon_Shout.ttf",FONT_SIZE)
        self.score_text = 0
        self.start_offset = 0
        # Menu setup
        menu      = pygame.image.load("../graphics/ui/menu.png").convert_alpha()
        self.menu = pygame.transform.rotozoom(menu,0,SCALE_FACTOR)
        self.menu_rect = self.menu.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        # Music 
        self.bg_music  = pygame.mixer.Sound("../musics/music.ogg")
        self.bg_music.play(loops=-1)

    def detect_collision(self):
        if self.plane.rect.top <= 0: self.do_end_game()
        if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False):
            if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask):
                self.do_end_game()

    def do_end_game(self):
        self.end_game = True
        self.plane.kill()
        for sprite in self.collision_sprites: 
            if sprite.sprite_type == "obstacle": sprite.kill()

    def draw_score(self):
        if not self.end_game: 
            self.score_text = (pygame.time.get_ticks()-self.start_offset)//1000
            score_y = WINDOW_HEIGHT/10
        else:
            score_y = WINDOW_HEIGHT/2 + self.menu_rect.height/1.5
        score      = self.font.render(f"{self.score_text}",True,SCORE_COLOR)
        score_rect = score.get_rect(midtop=(WINDOW_WIDTH/2,score_y))
        self.screen.blit(score,score_rect)

    def restart(self):
        self.end_game = False
        self.plane = Plane(self.all_sprites)
        self.start_offset = pygame.time.get_ticks()

    def run(self):
        prev_time = time.time()
        while True:
            dt        = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT                               : sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if not self.end_game: self.plane.jump()
                    else: self.restart()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not self.end_game: self.plane.jump()
                    else: self.restart()
                if event.type == self.obstacle_timer and not self.end_game:
                    Obstacle([self.all_sprites,self.collision_sprites])
            self.screen.fill(BACKGROUND_COLOR)
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.draw_score()
            if not self.end_game: 
                self.detect_collision()
            else:
                self.screen.blit(self.menu,self.menu_rect)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
>>>>>>> b5d4c06fe06fac9355bddf6676ca7acd835b2e79
    game.run()