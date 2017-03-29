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
    ACTION_NONE = 'NONE'
    ALL_ACTIONS = [ACTION_LEFT,
                   ACTION_RIGHT,
                   ACTION_UP,
                   ACTION_DOWN,
                   ACTION_NONE
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
        self.grid = self.__empty_grid()
        self.food = food.Food(numXCell, numYCell)
        self.snake = snake.Snake(0, 0, numXCell, numYCell)
        self.foodAgent = foodAgent()
        self.update()
        self.score = 0
        self.foodScore = 50
        self.livingScore = -1
        self.gameOver = False

    def getGrid(self):
        '''
        Returns a string containing the
        current grid configuration.
        '''
        w = self.numXCell
        h = self.numYCell
        s = ''
        grid = self.grid
        for x in range(0, h):
            for y in range(0, w):
                s += str(grid[x][y])
            s += '\n'
        return s[:-1]

    def isValidAction(self, action):
        '''
        Moving in reverse direction is not a valid action for
        snakes with length more than 1 cell.
        If the action causes motion in reverse direction,
        we return false.
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

    def executeAction(self):
        '''
        Move according to previously taken valid action. This updates
        the snakes cordinates and food cordinates, according to the
        existing direction of motion. This does
        not update the gameStateGrid.

        returns False if the snake has died, else returns True
        '''
        snake = self.snake
        # Move according to direction
        if not snake.update():
            self.gameOver = True
            return False
        # Snake is not dead, add livingScore and try to eat food
        self.score += self.livingScore
        x, y = self.food.getFoodCordinate()
        if(snake.eat(x, y)):
            fx, fy = self.foodAgent.getNextFoodCordinates(self)
            self.food.newFood(fx, fy)
            self.score += self.foodScore
        return True

    def update(self):
        '''
        Updates the internal grid configuration
        based on the snake and food positions.
        Call this after all actions that can potentially
        alter the grid configuration.
        '''
        self.grid = self.__empty_grid()
        grid = self.grid
        cords = self.food.getFoodCordinate()
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
        self.grid = grid

    def getScore(self):
        return self.score

    def getLegalActions(self):
        ret = []
        for action in self.ALL_ACTIONS:
            if self.isValidAction(action):
                ret.append(action)
        return ret

    def generateSnakeSuccessor(self, action):
        '''
        Generates the successor state after executing
        action. The current state is not modified.
        '''
        successorGameState = copy.deepcopy(self)
        successorGameState.chooseAction(action)
        successorGameState.executeAction()
        successorGameState.update()
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


def demo():
    gs = GameState(5, 4)
    print("Initial state followd by 4 LEFT motions.")
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    gs.update()
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    gs.update()
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    gs.update()
    print(gs.getGrid())
    print()
    gs.chooseAction('LEFT')
    gs.executeAction()
    gs.update()
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


if __name__ == "__main__":
    demo()
