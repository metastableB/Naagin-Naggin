#
# @author:Don Dennis (metastableB)
# food.py
#

from random import randint


class Food:

    def __init__(self, numXCell, numYCell, x = None, y = None):
        '''
        Initializes a food to random positoin. Positive x along
        width and positive y along top-down direction
        Random position generated can coincide with the snake.
        Make sure to escape this.

        :param: num_cell_x: Number of cells in x direction
        :param: num_cell_y: Number of cells in y direction
        '''
        self.X_MAX = numXCell
        self.Y_MAX = numYCell
        self.X_MIN = 0
        self.Y_MIN = 0
        self.x, self.y = x, y
        if None in [x, y]:
            self.x, self.y = self.__randomFood()

    def newFood(self, x, y):
        '''
        Places food in a new position
        x and y are cordinates.
        '''
        self.x, self.y = x, y

    def getFoodCordinate(self):
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

    def __randomFood(self):
        '''
        Private Method:
        Generates a new random position for the food
        '''
        x = randint(self.X_MIN, self.X_MAX - 1)
        y = randint(self.Y_MIN, self.Y_MAX - 1)
        return x, y


def demo():
    f1 = Food(2, 2, 1, 1)
    f2 = Food(2, 3, 2, 1)

    print("f1 init: " + str(f1.getFoodCordinate()))
    print("f2 init: " + str(f2.getFoodCordinate()))
    f1.newFood(2, 1)
    f2.newFood(1, 1)
    print("f1 new: " + str(f1.getFoodCordinate()))
    print("f2 new: " + str(f2.getFoodCordinate()))


if __name__ == "__main__":
    demo()
