#
# @author:Don Dennis (metastableB)
# foodAgent.py
#


from random import randint
from dlsnake.base.util import manhattanDistance


class FoodAgent:
    '''
    Base class for all agents controlling the food. All
    agents must define the getNextFoodCordinates() method which
    takes the current gameState as action. Also,
    all agents must define getLegalActions() method which
    returns the valid positions that the food can be placed
    in given the current game configuration.

    The food agent is part of the game rules and
    not an external player. Hence, design choices are
    often different from that of snakeAgents.
    '''

    def __init__(self):
        pass

    def getNextFoodCordinates(self, gameState):
        '''
        The agent will get a gameState object and must
        return a valid cordinate for food.
        '''
        pass

    def getLegalActions(self, gameState):
        pass

    def __isValidFood(self, foodCord, gameState):
        '''
        Check if foodCord is a valid cordinate for the food.
        Valid cordinates are those which has no conflicts with
        the snake or with any wall that may be present
        '''
        snakeCord = gameState.snake.getSnakeCordinateList()
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
        self.allCordinates = None

    def getNextFoodCordinates(self, gameState):
        '''
        Gets the next food cordinate according
        to the current agent.
        '''
        msg = 'FoodAgent.getNextFoodCordinates called even when '
        msg += 'food is already present!'
        # Make sure we are only called when there is no food
        assert None in gameState.getFoodCordinate(), msg
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

    def getLegalActions(self, gameState):
        '''
        Returns all valid moves the random agent
        can make, which is effectively all unoccupied
        cells. Moves will only be made if there is no
        food on the board. Otherwise, an empty list will
        be returned.
        '''
        if None not in gameState.getFoodCordinate():
            return []
        if self.allCordinates is None:
            possibleX = [x for x in range(0, gameState.numXCell)]
            possibleY = [y for y in range(0, gameState.numYCell)]
            import itertools
            lcord = itertools.product(possibleX, possibleY)
            self.allCordinates = list(lcord)
        allCord = self.allCordinates
        snakeCord = gameState.getSnakeCordinates()
        validCord = list(set(allCord) - set(snakeCord))
        return validCord


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
        msg = 'FoodAgent.getNextFoodCordinates called even when '
        msg += 'food is already present!'
        # Make sure we are only called when there is no food
        assert None in gameState.getFoodCordinate(), msg

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
            fx, fy = self.__getDiagonallyNext(fx, fy)
            validFood = self._FoodAgent__isValidFood((fx, fy), gameState)
            i += 1
        if validFood:
            return fx, fy
        while not validFood:
            fx, fy = self._FoodAgent__randomFood()
            validFood = self._FoodAgent__isValidFood((fx, fy), gameState)
        return fx, fy

    def getLegalActions(self, gameState):
        '''
        Returns all valid moves the random agent
        can make. To reduce the number of states
        returned by this method, the actual nextMove
        along with all diagonal cells are returned.
        The actual move can actually be random on
        account of all diagonally opposite cells
        and their neighbours being occupied.

        Also note that the next move that this agent
        makes need not necessarily be the best move
        according to your evaluation function.
        '''
        if None not in gameState.getFoodCordinate():
            return []
        nextCord = self.getNextFoodCordinates(gameState)
        validCord = list(self.corners)
        if nextCord not in validCord:
            validCord.append(nextCord)

        allCord = validCord
        snakeCord = gameState.getSnakeCordinates()
        validCord = list(set(allCord) - set(snakeCord))
        return validCord

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

    def __getDiagonallyNext(self, fx, fy):
        x = +1
        y = +1
        if fx > self.X_MAX - fx:
            x = -1
        if fy > self.Y_MAX - fy:
            y = -1
        return (fx + x, fy + y)
