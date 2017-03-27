#
# @author:Don Dennis (metastableB)
# gameState.py
#
from dlsnake import config
from dlsnake.base import food, snake
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
    SNAKE_CELL_VALUE = config.SNAKE_CELL_VALUE
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

    def __init__(self, numXCell, numYCell):
        '''
        Contains all the information about the
        current state of the game. Including
        information like maze/grid positions
        snake position, food etc
        '''
        self.numXCell = numXCell
        self.numYCell = numYCell
        self.grid = self.__empty_grid()
        self.food = food.Food(numXCell, numYCell)
        self.snake = snake.Snake(0, 0, numXCell, numYCell)
        self.update()
        # FIXME: score is currently part of snake
        # Should be part of gameState

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

    def chooseAction(self, action):
        '''
        Takes `action` on the gameState and updates
        the game state accordingly. Action is a movement
        key, either LEFT, RIGHT, UP or DOWN as defined in
        gameState.allActions

        '''
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

    def executeAction(self):
        '''
        Move according to previously taken action
        '''
        snake = self.snake
        # Move according to direction
        if not snake.update():
            return False
        # Snake is not dead, try to eat food
        x, y = self.food.getFoodCordinate()
        if(snake.eat(x, y)):
            self.food.newFood()
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
            grid[r_][c_] = self.SNAKE_CELL_VALUE
        self.grid = grid

    def getScore(self):
        return self.snake.score

    def getLegalActions(self):
        '''
        FIXME: all actions are legal
        '''
        return self.ALL_ACTIONS

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
