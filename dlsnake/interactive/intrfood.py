#
# @author:Don Dennis (metastableB)
# IntrFood.py
#

from dlsnake.base.food import Food
from dlsnake import config as cfg
import pygame


class IntrFood(Food):
    '''
    Interactive version of food, for display on
    pygame canvas
    '''
    FOOD_COLOR = cfg.COLOR_GREEN
    CELL_WIDTH = cfg.CELL_WIDTH

    def __init__(self):
        Food.__init__(self)

    def show(self, screen):
        x = self.x
        y = self.y
        xpix, ypix = self.__cell_to_pixels(x, y)
        self.__color_cell(screen, xpix, ypix, self.FOOD_COLOR)

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
        x = self.CELL_WIDTH * x
        y = self.CELL_WIDTH * y
        return x, y
