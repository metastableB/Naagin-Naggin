#
# @author:Don Dennis (metastableB)
# learnfood.py
#


from dlsnake.base.food import Food
from dlsnake import config as cfg


class LearnFood(Food):
    '''
    Learning version of food, for uisng
    in the deep learning model.
    '''
    FOOD_CELL_VALUE = cfg.FOOD_CELL_VALUE
    CELL_WIDTH = cfg.CELL_WIDTH

    def __init__(self):
        Food.__init__(self)

    def show(self, canvas_array):
        x = self.x
        y = self.y
        canvas_array[y][x] = self.FOOD_CELL_VALUE
