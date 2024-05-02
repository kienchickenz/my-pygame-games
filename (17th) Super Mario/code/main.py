from settings import *
from pytmx.util_pygame import load_pygame
import os.path

class Game:
    def __init__(self) -> None:
        # Defaults
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Super Mario - My 17th python game")

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q: 
                    pygame.quit()
                    sys.exit()
            
            # print(self.clock.tick(60))

if __name__ == "__main__":
    game = Game()
    game.run()