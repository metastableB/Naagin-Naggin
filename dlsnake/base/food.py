#
# @author:Don Dennis (metastableB)
# food.py
#

from random import randint
from dlsnake import config


class Food:
    X_MIN = config.X_MIN
    X_MAX = config.X_MAX
    Y_MIN = config.Y_MIN
    Y_MAX = config.Y_MAX

    def __init__(self):
        self.new_food()

    def new_food(self):
        '''
        Places food in a new position
        '''
        self.x, self.y = self.__random_food()

    def get_food(self):
        '''
        Returns the current cordinates of the food
        Cordinates specified in number of cells.
        '''
        return self.x, self.y

    def show(self):
        '''
        This function is to be called to show the food.
        Exactly how show is defined depends on the environment
        using it
        Override if necessary
        '''
        pass

    def __random_food(self):
        '''
        Private Method:
        Generates a new random position for the food
        '''
        x = randint(self.X_MIN, self.X_MAX)
        y = randint(self.Y_MIN, self.Y_MAX)
        return x, y


def demo():
    f1 = Food()
    f2 = Food()

    print("f1 init: " + str(f1.get_food()))
    print("f2 init: " + str(f2.get_food()))
    f1.new_food()
    f2.new_food()
    print("f1 new: " + str(f1.get_food()))
    print("f2 new: " + str(f2.get_food()))


if __name__ == "__main__":
    demo()
