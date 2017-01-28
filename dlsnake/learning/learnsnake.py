#
# @author:Don Dennis (metastableB)
# learnsnake.py
#

from dlsnake.base.snake import Snake
from dlsnake import config as cfg


class LearnSnake(Snake):
    '''
    Interactive version of snake, for display on
    pygame canvas
    '''
    SNAKE_CELL_VALUE = cfg.SNAKE_CELL_VALUE
    CELL_WIDTH = cfg.CELL_WIDTH

    def __init__(self, x, y):
        Snake.__init__(self, x, y)

    def show(self, screen_array):
        x = self.x
        y = self.y
        screen_array[y][x] = self.SNAKE_CELL_VALUE
