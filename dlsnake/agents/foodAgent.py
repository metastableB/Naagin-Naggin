#
# @author:Don Dennis (metastableB)
# foodAgent.py
#


from random import randint


class FoodAgent:
    '''
    Base class for all agents controlling the food. All
    agents must define the getFood() method which
    takes the current gamestate as action.

    The food agent is part of the game rules and
    not an external player. Hence, design choices are
    often different from that of snakeAgents.
    '''

    def __init__(self):
        pass

    def getNextFoodCordinates(self, gamestate):
        '''
        The agent will get a gamestate object and must
        return a valid cordinate for food.
        '''
        pass


class RandomFoodAgent(FoodAgent):
    '''
    Randomly selects a valid cordinate for food.
    '''

    def __init__(self):
        pass

    def getNextFoodCordinates(self, gameState):
        self.X_MAX = gameState.numXCell
        self.X_MIN = 0
        self.Y_MAX = gameState.numYCell
        self.Y_MIN = 0
        validFood = False
        while not validFood:
            fx, fy = self.__randomFood()
            validFood = self.__isValidFood((fx, fy), gameState)
        return fx, fy

    def __isValidFood(self, foodCord, gamestate):
        '''
        Check if foodCord is a valid cordinate for the food.
        Valid cordinates are those which has no conflicts with
        the snake or with any wall that may be present
        '''
        snakeCord = gamestate.snake.getSnakeCordinateList()
        if foodCord in snakeCord:
            return False
        return True

    def __randomFood(self):
        '''
        Private Method:
        Generates a new random position for the food
        '''
        x = randint(self.X_MIN, self.X_MAX - 1)
        y = randint(self.Y_MIN, self.Y_MAX - 1)
        return x, y
