#
# @author:Don Dennis (metastableB)
# intrsnake.py
#
from dlsnake.base.snake import Snake
from dlsnake import config as cfg
import pygame


class IntrSnake(Snake):
    '''
    Interactive version of snake, for display on
    pygame canvas
    '''
    SNAKE_COLOR = cfg.INTR_SNAKE_COLOR
    CELL_WIDTH = cfg.CELL_WIDTH

    def __init__(self, x, y):
        Snake.__init__(self, x, y)

    def show(self, screen):
        x = self.x
        y = self.y
        xpix, ypix = self.__cell_to_pixels(x, y)
        self.__color_cell(screen, xpix, ypix, self.SNAKE_COLOR)

    def __color_cell(self, screen, x, y, clr):
        '''
        Colors the box identified by x,y with color clr
        '''
        pygame.draw.rect(screen, clr, (x, y, self.CELL_WIDTH, self.CELL_WIDTH))

    def __cell_to_pixels(self, x, y):
        '''
        Converts cell indexes to corresponding cordinates
        of top left pixel
        returns x,y
        '''
        x = self.CELL_WIDTH*x
        y = self.CELL_WIDTH*y
        return x, y


def main():
    a = IntrSnake(1, 2)
    a.show()

if __name__ == "__main__":
    main()
