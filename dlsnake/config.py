#
# @author:Don Dennis (metastableB)
# config.py
#

# Width and height of the display window
DISP_WIDTH = 800
DISP_HEIGHT = 600

# Width of a square cell (this defines the size of the snake)
CELL_WIDTH = 40

# Boundaries of the canvas available to the snake
# for movement  specified in terms of
# cells. The snake takes cordinates in range (X,Y)_MIN to
# (X,Y)_MAX (exclusive).
X_MIN = 0
X_MAX = (DISP_WIDTH / CELL_WIDTH)
Y_MIN = 0
Y_MAX = (DISP_HEIGHT / CELL_WIDTH)

# Some color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
INTR_SNAKE_COLOR = COLOR_BLUE

GAME_FRAME_RATE = 10
