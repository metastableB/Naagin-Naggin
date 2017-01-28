#
# @author:Don Dennis (metastableB)
# gui_game.py
#


import pygame
import dlsnake.config as cfg
from dlsnake.interactive.intrsnake import IntrSnake
from dlsnake.interactive.intrfood import IntrFood

frameRate = cfg.GAME_FRAME_RATE


def main():
    gameDisplay = pygame.display.set_mode((cfg.DISP_WIDTH, cfg.DISP_HEIGHT))
    pygame.display.set_caption('Deep Learning Snake')
    clock = pygame.time.Clock()
    died = False
    s = IntrSnake(0, 0)
    f = IntrFood()
    while not died:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                died = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    s.direction(0, -1)
                if event.key == pygame.K_DOWN:
                    s.direction(0, 1)
                if event.key == pygame.K_LEFT:
                    s.direction(-1, 0)
                if event.key == pygame.K_RIGHT:
                    s.direction(1, 0)

        gameDisplay.fill(cfg.COLOR_WHITE)
        s.update()
        if s.eat(f.x, f.y):
            f.new_food()
        s.show(gameDisplay)
        f.show(gameDisplay)
        pygame.display.update()
        clock.tick(frameRate)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
