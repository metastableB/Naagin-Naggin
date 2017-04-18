#
# @author:Don Dennis (metastableB)
# gameState.py
#
from dlsnake import config
from dlsnake.base import food, snake
from dlsnake.agents.foodAgent import RandomFoodAgent
import copy


class GameState():
    '''
    Contains all the information about the
    current state of the game. Including
    information like maze/grid positions
    snake position, food etc
    '''
    EMPTY_CELL_VALUE = config.EMPTY_CELL_VALUE
    FOOD_CELL_VALUE = config.FOOD_CELL_VALUE
    SNAKE_BODY_CELL_VALUE = config.SNAKE_BODY_CELL_VALUE
    SNAKE_HEAD_CELL_VALUE = config.SNAKE_HEAD_CELL_VALUE
    ACTION_LEFT = 'LEFT'
    ACTION_RIGHT = 'RIGHT'
    ACTION_UP = 'UP'
    ACTION_DOWN = 'DOWN'
    ALL_ACTIONS = [ACTION_LEFT,
                   ACTION_RIGHT,
                   ACTION_UP,
                   ACTION_DOWN,
                   ]

    def __init__(self, numXCell, numYCell, foodAgent=RandomFoodAgent):
        '''
        Contains all the information about the
        current state of the game. Including
        information like maze/grid positions
        snake position, food etc

        The foodAgent is a part of the game rules
        and not the external world, hence it is
        included as part of the gameState object.
        '''
        self.numXCell = numXCell
        self.numYCell = numYCell
        self.food = food.Food(numXCell, numYCell)
        self.snake = snake.Snake(0, 0, numXCell, numYCell)
        self.foodAgent = foodAgent()
        self.score = 0
        self.foodScore = 50  # 0.5
        self.livingScore = -1  # -0.005
        self.completionScore = 500  # 1.0
        self.gameOver = False
        self.gameComplete = False
        self.collisionScore = -50  # -0.5
        self.minAllowedScore = -50  # -2.0

    def getGrid(self):
        '''
        Returns a string containing the
        current grid configuration.
        '''
        grid = self.__getUpdatedGrid()
        w = self.numXCell
        h = self.numYCell
        s = ''
        for x in range(0, h):
            for y in range(0, w):
                if grid[x][y] != self.EMPTY_CELL_VALUE:
                    s += str(grid[x][y])
                else:
                    s += '.'
            s += '\n'
        return s[:-1]

    def isValidAction(self, action):
        '''
        Moving in reverse direction is not a valid action for
        snakes with length more than 1 cell.
        If the action causes motion in reverse direction,
        we return false.

        Here validity is defined in terms of the rules of the
        game. Hence choosing to run into ones on body or a wall
        are perfectly valid actions according to game rules.
        '''
        snake = self.snake
        if len(snake.getSnakeCordinateList()) == 1:
            return True

        if action not in self.ALL_ACTIONS:
            raise ValueError('Specified action not part of `allActions`')

        currDir = snake.getCurrentDirection()
        if action == self.ACTION_UP and currDir == (0, 1):
            return False
        elif action == self.ACTION_DOWN and currDir == (0, -1):
            return False
        elif action == self.ACTION_LEFT and currDir == (1, 0):
            return False
        elif action == self.ACTION_RIGHT and currDir == (-1, 0):
            return False
        return True

    def chooseAction(self, action):
        '''
        Takes `action` on the gameState and updates
        the snakes direction accordingly. Action is a movement
        key, either LEFT, RIGHT, UP or DOWN as defined in
        gameState.allActions. The snake's direction is updated
        but the snakes cordinates are not updated. Hence
        if multiple chooseAction() is called, only the last
        called valid action will have any effect.
        '''
        if not self.isValidAction(action):
            return False
        # Change the direction
        snake = self.snake
        if action not in self.ALL_ACTIONS:
            raise ValueError('Specified action not part of `allActions`')
        if action == self.ACTION_UP:
            snake.direction(0, -1)
        if action == self.ACTION_DOWN:
            snake.direction(0, 1)
        if action == self.ACTION_LEFT:
            snake.direction(-1, 0)
        if action == self.ACTION_RIGHT:
            snake.direction(1, 0)
        return True

    def executeAction(self, newFood=True):
        '''
        Move according to previously taken valid action. This updates
        the snakes cordinates and food cordinates, according to the
        existing direction of motion. This does
        not update the gameStateGrid.

        if newFood is set to False, no new food will be generated
        even if the snake eats the food. If the snake eats the food,
        new food is set to None
        returns False if the game ended, else returns True
        '''
        snake = self.snake
        # Move according to direction
        if not snake.update():
            self.gameOver = True
            self.score += self.collisionScore
            return False
        # Snake is not dead, add livingScore and try to eat food
        self.score += self.livingScore
        x, y = self.food.getFoodCordinate()
        if(snake.eat(x, y)):
            self.food.newFood(None, None)
            if newFood:
                fx, fy = self.foodAgent.getNextFoodCordinates(self)
                if None in (fx, fy):
                    self.gameOver = True
                    self.gameComplete = True
                    self.score += self.completionScore
                    return False
                self.food.newFood(fx, fy)
            self.score += self.foodScore

        if(self.score < self.minAllowedScore):
            self.gameOver = True
            self.score += self.collisionScore
            return False
        return True

    def getScore(self):
        return self.score

    def getLegalActionsSnake(self):
        '''
        Returns a list of legal actions that the
        snake can make. The actions will be a subset
        of self.ALL_ACTIONS
        '''
        ret = []
        for action in self.ALL_ACTIONS:
            if self.isValidAction(action):
                ret.append(action)
        return ret

    def getLegalActionsFoodAgent(self):
        '''
        Returns a list of cordinates which are
        valid positions for the current foodAgent
        to place food. The definition of validity
        depends on the foodAgent being used. For
        the RandomFoodAgent, all unoccupied cells
        are valid.
        '''
        foodCord = self.getFoodCordinate()
        if None in foodCord:
            return self.foodAgent.getLegalActions(self)
        else:
            return []

    def generateSuccessor(self, action, newFood = True):
        '''
        Generates the successor state after executing
        action for snake and foodAgent. The current
        state is not modified and a new GameState
        instance is returned.
        '''
        successorGameState = copy.deepcopy(self)
        successorGameState.chooseAction(action)
        successorGameState.executeAction(newFood)
        return successorGameState

    def generateSnakeSuccessor(self, action):
        return self.generateAgentSuccessor(0, action)

    def generateFoodAgentSuccessor(self, action):
        return self.generateAgentSuccessor(1, action)

    def generateAgentSuccessor(self, agent, action):
        '''
        Generates the successor state after execution
        action for agent. If agent=0, indicating
        snake, the actions should be part of
        gameState.ALL_ACTIONS. If instead, agent=1, the
        foodAgent, then action should be a legal cordinate
        for placing the food packet
        '''
        successorGameState = copy.deepcopy(self)
        if agent not in [0, 1]:
            raise ValueError("Agent Should be either 0 or 1.")
        if agent == 0:
            foodCord = self.getFoodCordinate()
            msg = 'There is no food on the grid!'
            msg += ' Did the foodAgent get a chance to act?'
            assert None not in foodCord, msg
            successorGameState.chooseAction(action)
            successorGameState.executeAction(newFood=False)
            return successorGameState
        elif agent == 1:
            foodCord = self.getFoodCordinate()
            msg = 'There is food on the grid!'
            msg += ' Why is foodAgent trying to add more food?'
            assert None in foodCord or foodCord == action, msg
            # We don't have food
            fx, fy = action
            successorGameState.food.newFood(fx, fy)
            return successorGameState

    def getFoodCordinate(self):
        '''
        Returns the current cordinate of food
        '''
        return self.food.getFoodCordinate()

    def getSnakeHeadCordinate(self):
        '''
        Returns the cordinate to the head of the
        snake
        '''
        return self.snake.getHead()

    def getSnakeCordinates(self):
        '''
        Returns a list of coordinates occupied
        by the snake.
        '''
        return self.snake.getSnakeCordinateList()

    def getSnakeLength(self):
        return self.snake.getSnakeLength()

    def setFoodScore(self, value):
        '''
        Set the score the snake gets when
        a food is eatern.
        '''
        self.foodScore = value

    def setLivingScore(self, value):
        '''
        Sets the living score (can be negative). After
        each move, this value is added to the snake.
        '''
        self.livingScore = value

    def getCurrentDirection(self):
        '''
        Returns the current direction of motion of the snake.
        Returned values among gameState.possibleActions
        '''
        currDir = self.snake.getCurrentDirection()
        if currDir == (0, -1):
            return self.ACTION_UP
        elif currDir == (0, 1):
            return self.ACTION_DOWN
        elif currDir == (-1, 0):
            return self.ACTION_LEFT
        elif currDir == (1, 0):
            return self.ACTION_RIGHT

    '''
    PRIVATE METHODS
    '''

    def __empty_grid(self):
        row = [self.EMPTY_CELL_VALUE for x in range(0, self.numXCell)]
        grid = [list(row) for x in range(0, self.numYCell)]
        return grid

    def __cordsToIndex(self, list_cordinates):
        '''
        Takes a list of cordinates and convert
        them to the corresponding index in the internal
        grid so that they can be accessed.

        :param: list_cordinates: list of cordinates to convert
        '''
        ret = []
        for cordinate in list_cordinates:
            (x, y) = cordinate
            ret.append((y, x))
        return ret

    def __getUpdatedGrid(self):
        '''
        This method is private to facillitate lazy evaluation.
        getGrid() should be used as the interface for viewing
        the updated grid. getGrid() automatically calls
        this method internally.

        Updates the internal grid configuration
        based on the snake and food positions.
        Call this after all actions that can potentially
        alter the grid configuration.
        '''
        grid = self.__empty_grid()
        cords = self.food.getFoodCordinate()
        if None not in cords:
            positions = self.__cordsToIndex([cords])
            for pos in positions:
                r_, c_ = pos
                grid[r_][c_] = self.FOOD_CELL_VALUE
        cords = self.snake.getSnakeCordinateList()
        positions = self.__cordsToIndex(cords)
        for pos in positions:
            r_, c_ = pos
            grid[r_][c_] = self.SNAKE_BODY_CELL_VALUE
        cords = self.snake.getHead()
        pos = self.__cordsToIndex([cords])
        r_, c_ = pos[0]
        grid[r_][c_] = self.SNAKE_HEAD_CELL_VALUE
        return grid


def demo():
    gs = GameState(5, 4)
    print("Initial state followd by 4 LEFT motions.")
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    print(gs.getGrid())
    print()

    print("generating Successor for DOWN")
    succ = gs.generateSnakeSuccessor("DOWN")
    print("Original")
    print(gs.getGrid())
    print()
    print("Successor")
    print(succ.getGrid())
    print()
    print(dir(gs))


if __name__ == "__main__":
    demo()
