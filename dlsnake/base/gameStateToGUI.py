#
# @author:Don Dennis (metastableB)
# gameStateToGUI.py
#
import pygame
from dlsnake import config as cfg


class GameStateToGUI:
    '''
    Converts a grid representation of game state
    to a GUI representation
    '''
    '''
    FIXME: These should be an arguments
    '''
    FOOD_COLOR = cfg.COLOR_GREEN
    SNAKE_BODY_COLOR = cfg.COLOR_BLUE
    SNAKE_HEAD_COLOR = cfg.COLOR_LIGHT_GREEN
    FONT_COLOR = cfg.COLOR_RED
    gameOverMessage = "Game Over!"
    completionMessage = "Game Completed!"

    def __init__(self, gameState, cellWidth, frameRate=cfg.GAME_FRAME_RATE):
        '''
        The gameState object to attach to and the
        width of a single cell interms of its pixels
        '''
        self.gameState = gameState
        self.cellWidth = cellWidth
        self.frameRate = frameRate
        self.canvasWidth = cellWidth * gameState.numXCell
        self.canvasHeight = cellWidth * gameState.numYCell
        self.gameDisplay = pygame.display.set_mode(
            (self.canvasWidth, self.canvasHeight))
        pygame.display.set_caption('Deep Learning Snake')
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.scoreFont = pygame.font.SysFont('Comic Sans MS', self.cellWidth)
        self.died = False

    def show(self):
        '''
        Display the current grid configuration.
        '''
        gameDisplay = self.gameDisplay
        gameDisplay.fill(cfg.COLOR_WHITE)
        self.__drawFood()
        self.__drawSnake()
        self.__drawScore()
        self.__drawMessage()
        pygame.display.update()
        self.clock.tick(self.frameRate)

    '''
    PRIVATE METHODS
    '''

    def __drawMessage(self):
        message = None
        if self.gameState.gameComplete:
            message = self.completionMessage
        elif self.gameState.gameOver:
            message = self.gameOverMessage
        else:
            return

        self.gameOverMessageSurface = self.scoreFont.render(
            message, False, self.FONT_COLOR)
        pos_x = self.canvasWidth / 2 - 2 * self.cellWidth
        pos_y = self.canvasHeight / 2
        pos = (pos_x, pos_y)
        self.gameDisplay.blit(self.gameOverMessageSurface, pos)

    def __drawScore(self):
        length = self.gameState.getSnakeLength()
        scoreStr = "Len: " + str(length)
        score = self.gameState.getScore()
        scoreStr += "  Score: " + str(score)
        score = str(scoreStr)
        self.scoresurface = self.scoreFont.render(
            score, False, self.FONT_COLOR)
        pos_x = self.canvasWidth - 8 * self.cellWidth
        pos_y = 0.2 * self.cellWidth
        pos = (pos_x, pos_y)
        self.gameDisplay.blit(self.scoresurface, pos)

    def __drawSnake(self):
        cordinates = self.gameState.snake.getSnakeCordinateList()
        for cordinate in cordinates:
            x, y = cordinate
            xpix, ypix = self.__cell_to_pixels(x, y)
            self.__color_cell(xpix, ypix, self.SNAKE_BODY_COLOR)
        x_, y_ = self.gameState.snake.getHead()
        xpix, ypix = self.__cell_to_pixels(x_, y_)
        self.__color_cell(xpix, ypix, self.SNAKE_HEAD_COLOR)

    def __drawFood(self):
        x, y = self.gameState.food.getFoodCordinate()
        # If the game has no food!
        if None in (x, y):
            return
        xpix, ypix = self.__cell_to_pixels(x, y)
        self.__color_cell(xpix, ypix, self.FOOD_COLOR)

    def __color_cell(self, x, y, clr):
        '''
        Colors the box identified by x,y with color clr
        '''
        screen = self.gameDisplay
        border = 2
        boundingBox = (x + border, y + border, self.cellWidth -
                       border, self.cellWidth - border)
        pygame.draw.rect(screen, clr, boundingBox)

    def __cell_to_pixels(self, x, y):
        '''
        Converts cell indexes to corresponding cordinates
        of top left pixel
        returns x,y
        '''
        x = self.cellWidth * x
        y = self.cellWidth * y
        return x, y
