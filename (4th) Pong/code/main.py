import pygame,sys
from settings import *
from random   import choice
class Block(pygame.sprite.Sprite):
    def __init__(self,path,pos_x,pos_y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect  = self.image.get_rect(center=(pos_x,pos_y))

class Player(Block):
    def __init__(self,path,pos_x,pos_y,speed):
        super().__init__(path,pos_x,pos_y)
        self.speed = speed
        self.direction = None
    def update(self,ball_group):
        if self.direction == "up"   : self.rect.top    = max(self.rect.top-self.speed,0)
        if self.direction == "down" : self.rect.bottom = min(self.rect.bottom+self.speed,WINDOW_HEIGHT)

class Ball(Block):
    def __init__(self,path,pos_x,pos_y,speed,paddles):
        super().__init__(path,pos_x,pos_y)
        self.speed = speed
        self.velocity_x = speed*choice([-1,1])
        self.velocity_y = speed*choice([-1,1])
        self.paddles = paddles
        self.score_time = 0
        self.active     = False
        self.plob_sound  = pygame.mixer.Sound("../musics/pong.ogg")
        self.score_sound = pygame.mixer.Sound("../musics/score.ogg")
    def update(self):
        if self.active:
            if self.hit_top() or self.hit_bottom(): 
                self.velocity_y *= -1
                self.plob_sound.play()
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.bounce()
        else: 
            self.restart_counter()
    def hit_top(self)   : return self.rect.top <= 0
    def hit_bottom(self): return self.rect.bottom >= WINDOW_HEIGHT
    def bounce(self):
        if pygame.sprite.spritecollide(self,self.paddles,False):
            self.plob_sound.play()
            self.velocity_x *= -1
    def reset_ball(self):
        self.active = False
        self.velocity_x = self.speed*choice([-1,1])
        self.velocity_y = self.speed*choice([-1,1])
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        self.score_sound.play()
    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 0
        if current_time - self.score_time < DELAY_AFTER_SCORE/3:
            countdown_number = 3
        if DELAY_AFTER_SCORE/3 < current_time - self.score_time < DELAY_AFTER_SCORE*2/3:
            countdown_number = 2
        if DELAY_AFTER_SCORE*2/3 < current_time - self.score_time < DELAY_AFTER_SCORE:
            countdown_number = 1
        if current_time - self.score_time > DELAY_AFTER_SCORE:
            self.active = True
            return self.active
        time_counter = countdown_font.render(str(countdown_number),True,TEXT_COLOR)
        time_counter_rect = time_counter.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2-COUNTDOWN_OFFSET))
        screen.blit(time_counter,time_counter_rect)

class Opponent(Block):
    def __init__(self,path,pos_x,pos_y,speed):
        super().__init__(path,pos_x,pos_y)
        self.speed = speed
    def update(self,ball_sprite):
        if self.rect.top < ball_sprite.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_sprite.sprite.rect.y:
            self.rect.y -= self.speed

class Main:
    def __init__(self,ball_sprite,paddle_group):
        self.player_score   = 0
        self.opponent_score = 0
        self.ball_sprite = ball_sprite
        self.paddle_group = paddle_group
    def draw(self):
        middle_line = pygame.Rect((WINDOW_WIDTH/2-2,0),(LINE_WIDTH,WINDOW_HEIGHT))
        pygame.draw.rect(screen,LINE_COLOR,middle_line)
        self.paddle_group.draw(screen)
        self.ball_sprite.draw(screen)
        self.draw_score()
    def draw_score(self):
        player_score      = font.render(str(self.player_score),True,TEXT_COLOR)
        player_score_rect = player_score.get_rect(center=(WINDOW_WIDTH/2-SCORE_OFFSET,WINDOW_HEIGHT/2)) 
        opponent_score = font.render(str(str(self.opponent_score)),True,TEXT_COLOR)
        opponent_score_rect = opponent_score.get_rect(center=(WINDOW_WIDTH/2+SCORE_OFFSET,WINDOW_HEIGHT/2))
        screen.blit(player_score,player_score_rect)
        screen.blit(opponent_score,opponent_score_rect)
    def run(self):
        self.paddle_group.update(self.ball_sprite)
        self.ball_sprite.update()
        self.reset_ball()
    def reset_ball(self):
        if self.ball_sprite.sprite.rect.right >= WINDOW_WIDTH:
            self.player_score += 1
            self.ball_sprite.sprite.reset_ball()
        if self.ball_sprite.sprite.rect.left <= 0:
            self.opponent_score += 1
            self.ball_sprite.sprite.reset_ball()

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My forth python game")
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock  = pygame.time.Clock()
font           = pygame.font.Font("../fonts/Dunkin.otf",FONT_SIZE)
countdown_font = pygame.font.Font("../fonts/Dunkin.otf",COUNTDOWN_SIZE)
player   = Player("../graphics/paddle.png",PADDLE_OFFSET,WINDOW_HEIGHT/2,PLAYER_SPEED)
opponent = Opponent("../graphics/paddle.png",WINDOW_WIDTH-PADDLE_OFFSET,WINDOW_HEIGHT/2,OPPONENT_SPEED)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)
ball = Ball("../graphics/ball.png",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,BALL_SPEED,paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)
main = Main(ball_sprite,paddle_group)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT                               : sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP  : player.direction = "up"
            if event.key == pygame.K_DOWN: player.direction = "down"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP  : player.direction = None
            if event.key == pygame.K_DOWN: player.direction = None
    screen.fill(BG_COLOR)
    main.draw()
    main.run()
    pygame.display.update()
    clock.tick(FPS)