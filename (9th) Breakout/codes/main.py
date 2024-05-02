import pygame,sys,time
from settings import *
from sprites  import Player,Ball,Block,Upgrade,Projectile
from surfacemaker import SurfaceMaker
from pygame.math import Vector2
from random import choice,randint

class Game:
    def __init__(self):
        # Defaults
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.init()
        pygame.display.set_caption("My nineth python game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        
        self.bg = self.create_bg()
        # Groups
        self.all_sprites   = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        # Setup
        self.surfacemaker = SurfaceMaker()
        self.stage_setup()
        self.player = Player(self.all_sprites,self.surfacemaker)
        self.ball = Ball(
                        groups=self.all_sprites,
                        player=self.player,
                        blocks=self.block_sprites
                        )
        # Images
        self.heart_image = pygame.image.load("../graphics/other/heart.png").convert_alpha()
        self.projectile_image = pygame.image.load("../graphics/other/projectile.png").convert_alpha()
        self.can_shoot = True
        self.shoot_time = 0
        self.crt = CRT()
        # Musics
        self.bg_music = pygame.mixer.Sound("../musics/music.ogg")
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound("../musics/laser.ogg")
        self.laser_sound.set_volume(0.1)
        self.laser_hit_sound = pygame.mixer.Sound("../musics/laser_hit.ogg") 
        self.laser_hit_sound.set_volume(0.02)
        self.power_up_sound = pygame.mixer.Sound("../musics/powerup.ogg")
        self.power_up_sound.set_volume(0.1)

    def create_bg(self):
        original_bg   = pygame.image.load("../graphics/other/bg.png").convert()
        original_size = Vector2(original_bg.get_width(),original_bg.get_height())
        scale_factor  = WINDOW_HEIGHT/original_bg.get_height()
        scaled_size = original_size*scale_factor 
        scaled_bg   = pygame.transform.scale(original_bg,(scaled_size))
        return scaled_bg

    def stage_setup(self):
        for row_index,row in enumerate(BLOCK_MAP):
            for col_index,col in enumerate(row):
                if col != " ":
                    y = TOP_OFFSET + row_index * (BLOCK_HEIGHT+GAP_SIZE) + GAP_SIZE//2
                    x = col_index * (BLOCK_WIDTH +GAP_SIZE) + GAP_SIZE//2
                    Block(
                        groups=[self.all_sprites,self.block_sprites],
                        block_type=col,
                        pos=(x,y),
                        surfacemaker=self.surfacemaker,
                        create_upgrade=self.create_upgrade
                        )

    def display_heart(self):
        for i in range(self.player.hearts):
            x = 2 +  i * (self.heart_image.get_width() + 2)
            self.screen.blit(self.heart_image,(x,4))

    def create_upgrade(self,pos):
        upgrade_type = choice(UPGRADES)
        Upgrade([self.all_sprites,self.upgrade_sprites],pos,upgrade_type)

    def upgrade_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self.player,self.upgrade_sprites,True)
        for sprite in collision_sprites:
            self.player.upgrade(sprite.upgrade_type)
            self.power_up_sound.play()

    def create_projectile(self):
        self.laser_sound.play()
        for projectile in self.player.laser_rects:
            Projectile(
                    [self.all_sprites,self.projectile_sprites],
                    projectile.midtop-Vector2(0,30),
                    self.projectile_image
                    )

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= 750:
                self.can_shoot = True

    def projectile_collision(self):
        for projectile in self.projectile_sprites:
            collision_sprites = pygame.sprite.spritecollide(projectile,self.block_sprites,False)
            if collision_sprites:
                projectile.kill()
                self.laser_hit_sound.play()
                for block in collision_sprites:
                    block.get_damage(1)

    def run(self): 
        prev_time = time.time() 
        while True:
            # Delta time
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type==pygame.QUIT                             : sys.exit()     
                if event.type==pygame.KEYDOWN and event.key==pygame.K_q: sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        if not self.ball.active: self.ball.active = True
                        if self.can_shoot: 
                            self.create_projectile()
                            self.can_shoot = False
                            self.shoot_time = pygame.time.get_ticks()
            self.screen.blit(self.bg,(0,0))
            # Update
            self.all_sprites.update(dt)
            self.laser_timer()
            # Collision
            self.upgrade_collision()
            self.projectile_collision()
            # Draw
            self.all_sprites.draw(self.screen)
            self.display_heart()
            self.crt.draw()
            pygame.display.update()

class CRT:
    def __init__(self):
        vignette = pygame.image.load("../graphics/other/tv.png").convert_alpha()
        self.scaled_vignette = pygame.transform.scale(vignette,(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.screen = pygame.display.get_surface()
        self.create_crt_lines()

    def create_crt_lines(self):
        line_height = 4
        line_amount = WINDOW_HEIGHT//line_height
        for line in range(line_amount):
            y = line*line_height
            pygame.draw.line(
                self.scaled_vignette,
                (20,20,20),
                start_pos=(0,y),
                end_pos=(WINDOW_WIDTH,y),
                width=1
                )

    def draw(self):
        self.scaled_vignette.set_alpha(randint(60,75))
        self.screen.blit(self.scaled_vignette,(0,0))

if __name__ == "__main__":
    game = Game()
    game.run()