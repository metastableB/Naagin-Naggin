#
# @author:Don Dennis (metastableB)
# foodAgent.py
#


from random import randint
from dlsnake.base.util import manhattanDistance


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


class RandomFoodAgent(FoodAgent):
    '''
    Randomly selects a valid cordinate for food.
    '''

    def __init__(self):
        self.X_MAX = None
        self.X_MIN = None
        self.Y_MAX = None
        self.Y_MIN = None

    def getNextFoodCordinates(self, gameState):
        if self.X_MAX is None:
            self.X_MAX = gameState.numXCell
            self.X_MIN = 0
            self.Y_MAX = gameState.numYCell
            self.Y_MIN = 0
        validFood = False
        while not validFood:
            fx, fy = self._FoodAgent__randomFood()
            validFood = self._FoodAgent__isValidFood((fx, fy), gameState)
        return fx, fy


class MaxManhattanFoodAgent(FoodAgent):
    '''
    Agent tries to place the food such that the manhattan distance
    between the head of the snake and the new food cordinate
    is maximum
    '''

    def __init__(self):
        self.X_MAX = None
        self.X_MIN = None
        self.Y_MAX = None
        self.Y_MIN = None
        self.corners = []
        self.__makeCornerCordinates()

    def getNextFoodCordinates(self, gameState):
        if self.X_MAX is None:
            self.X_MAX = gameState.numXCell
            self.X_MIN = 0
            self.Y_MAX = gameState.numYCell
            self.Y_MIN = 0
            self.__makeCornerCordinates()

        # find which corner the snake head is in
        # and select the opposite corner
        # if invalid:
        #   diagonally work for 5 moves
        # if still invalid:
        #   select randomly and return
        head = gameState.snake.getHead()
        corners = self.corners
        distances = [manhattanDistance(head, corner) for corner in corners]
        maxIndex = distances.index(max(distances))
        foodCords = corners[maxIndex]
        validFood = self._FoodAgent__isValidFood(foodCords, gameState)
        if validFood:
            return foodCords
        # The corner is occupied
        fx, fy = foodCords
        i = 0
        while not validFood and i < 5:
            # FIXME: need to consider X_MIN
            fx += 1
            fx %= self.X_MAX
            fy += 1
            fy %= self.Y_MAX
            validFood = self._FoodAgent__isValidFood((fx, fy), gameState)
            i += 1
        if validFood:
            return fx, fy
        while not validFood:
            fx, fy = self._FoodAgent__randomFood()
            validFood = self._FoodAgent__isValidFood((fx, fy), gameState)
        return fx, fy

    def __makeCornerCordinates(self):
        X_MAX = self.X_MAX
        Y_MAX = self.Y_MAX
        X_MIN = self.X_MIN
        Y_MIN = self.Y_MIN
        self.corners = []
        if None in [X_MAX, Y_MAX, X_MIN, Y_MIN]:
            return
        self.corners.append((X_MIN, Y_MIN))
        self.corners.append((X_MIN, Y_MAX - 1))
        self.corners.append((X_MAX - 1, Y_MAX - 1))
        self.corners.append((X_MAX - 1, Y_MIN))
