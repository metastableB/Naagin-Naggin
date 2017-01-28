#
# @author:Don Dennis (metastableB)
# gui_game.py
#


import pygame
import dlsnake.config as cfg
from dlsnake.interactive.intrsnake import IntrSnake

frameRate = cfg.GAME_FRAME_RATE

def main():
    gameDisplay = pygame.display.set_mode((cfg.DISP_WIDTH, cfg.DISP_HEIGHT))
    pygame.display.set_caption('Deep Learning Snake')
    clock = pygame.time.Clock()
    died = False
    s = IntrSnake(0,0)
    while not died:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                died = True

        gameDisplay.fill(cfg.COLOR_WHITE)
        s.update()
        s.show(gameDisplay)
        pygame.display.update()
        clock.tick(frameRate)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
