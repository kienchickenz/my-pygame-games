import pygame,sys,random
from settings    import *
from pygame.math import Vector2
class SNAKE:
    def __init__(self):
        self.head_down  = pygame.image.load("graphics/head_down.png").convert_alpha()
        self.head_left  = pygame.image.load("graphics/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("graphics/head_right.png").convert_alpha()
        self.head_up    = pygame.image.load("graphics/head_up.png").convert_alpha()
        self.tail_down  = pygame.image.load("graphics/tail_up.png").convert_alpha()
        self.tail_left  = pygame.image.load("graphics/tail_right.png").convert_alpha()
        self.tail_right = pygame.image.load("graphics/tail_left.png").convert_alpha()
        self.tail_up    = pygame.image.load("graphics/tail_down.png").convert_alpha()
        self.body_horizontal = pygame.image.load("graphics/body_horizontal.png").convert_alpha()
        self.body_vertical   = pygame.image.load("graphics/body_vertical.png").convert_alpha()
        self.body_tr = pygame.image.load("graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("graphics/body_bl.png").convert_alpha()
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.grow = False
        self.crunch_sound = pygame.mixer.Sound("musics/crunch.ogg")
    
    def draw(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            x_pos = block.x*CELL_SIZE
            y_pos = block.y*CELL_SIZE
            block_rect = pygame.Rect((x_pos,y_pos),(CELL_SIZE,CELL_SIZE))
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                prev_block = self.body[index-1]-block
                next_block = self.body[index+1]-block
                if   prev_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1): 
                        screen.blit(self.body_tl,block_rect) # Top left 
                    if (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_tr,block_rect) # Top right
                    if (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_br,block_rect) # Bottom right
                    if (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_bl,block_rect) # Bottom left
    
    def update_tail_graphics(self):
        current_direction = self.body[-2] - self.body[-1]
        if   current_direction == Vector2(0,-1): self.tail = self.tail_up
        elif current_direction == Vector2(0,1) : self.tail = self.tail_down
        elif current_direction == Vector2(1,0) : self.tail = self.tail_right
        elif current_direction == Vector2(-1,0): self.tail = self.tail_left
    
    def update_head_graphics(self):
        current_direction = self.body[0] - self.body[1]
        if   current_direction == Vector2(0,-1): self.head = self.head_up
        elif current_direction == Vector2(0,1) : self.head = self.head_down
        elif current_direction == Vector2(1,0) : self.head = self.head_right
        elif current_direction == Vector2(-1,0): self.head = self.head_left
    
    def move(self):
        body_copy = self.body[:] if self.grow else self.body[:-1]
        self.grow = False
        body_copy.insert(0,body_copy[0]+self.direction)
        self.body = body_copy[:]
    
    def add(self): 
        self.grow = True

    def play_sound(self): 
        self.crunch_sound.play()

    def reset(self): 
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.fruit = pygame.image.load("graphics/apple.png").convert_alpha()
        self.randomize()
    
    def draw(self):
        pos_x = CELL_SIZE*self.pos.x
        pos_y = CELL_SIZE*self.pos.y
        fruit_rect = pygame.Rect((pos_x,pos_y),(CELL_SIZE,CELL_SIZE))
        screen.blit(self.fruit,fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0,WIDTH_IN_CELLS-1)
        self.y = random.randint(0,HEIGHT_IN_CELLS-1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move()
        self.detect_collision()
        self.detect_end_game()
   
    def draw(self):
        self.draw_grass()
        self.snake.draw()
        self.fruit.draw()
        self.draw_score()
   
    def draw_grass(self):
        for row in range(HEIGHT_IN_CELLS):
            if row % 2 == 0:
                for col in range(WIDTH_IN_CELLS):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect((CELL_SIZE*col,CELL_SIZE*row),(CELL_SIZE,CELL_SIZE))
                        pygame.draw.rect(screen,GRASS_COLOR,grass_rect)
            else:
                for col in range(WIDTH_IN_CELLS):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect((CELL_SIZE*col,CELL_SIZE*row),(CELL_SIZE,CELL_SIZE))
                        pygame.draw.rect(screen,GRASS_COLOR,grass_rect)
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score = font.render(score_text,True,SCORE_COLOR)
        score_rect = score.get_rect(topright=(SCORE_X,SCORE_Y))
        fruit_rect = self.fruit.fruit.get_rect(midright=(score_rect.left,score_rect.centery))
        score_bg_rect = pygame.Rect((fruit_rect.left,fruit_rect.top),((fruit_rect.width+score_rect.width+7),fruit_rect.height))
        pygame.draw.rect(screen,SCORE_BG_COLOR,score_bg_rect)
        pygame.draw.rect(screen,SCORE_COLOR,score_bg_rect,3)
        screen.blit(score,score_rect)
        screen.blit(self.fruit.fruit,fruit_rect)

    def detect_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add()
            self.snake.play_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos: self.fruit.randomize()
    
    def detect_end_game(self):
        if self.is_end_game(): self.end_game() 
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]: self.end_game()
    
    def is_end_game(self):
        return (not 0 <= self.snake.body[0].x < WIDTH_IN_CELLS) or (not 0 <= self.snake.body[0].y < HEIGHT_IN_CELLS)
    
    def end_game(self):
        self.snake.reset()

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("My second python game")
screen = pygame.display.set_mode((WIDTH_IN_CELLS*CELL_SIZE,HEIGHT_IN_CELLS*CELL_SIZE))
clock  = pygame.time.Clock()
font  = pygame.font.Font("fonts/PoetsenOne-Regular.ttf",TEXT_SIZE)
snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update,SNAKE_UPDATE)
main_game = MAIN()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT                               : sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()
        if event.type == snake_update: main_game.update()
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP   : 
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                case pygame.K_DOWN : 
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                case pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1: 
                        main_game.snake.direction = Vector2(1,0)
                case pygame.K_LEFT : 
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
    screen.fill(BACKGROUND_COLOR)
    main_game.draw()
    pygame.display.update()
    clock.tick(FPS)