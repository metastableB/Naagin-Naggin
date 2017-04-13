#
# @author:Don Dennis (metastableB)
# config.py
#

# Number of cells along width (+x) and height (+y)
NUM_X_CELL = 10
NUM_Y_CELL = 10

# Pixel width of cell (cells are squares)
CELL_WIDTH = 30

# Some color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_LIGHT_GREEN = (102, 153, 204)
COLOR_BLUE = (0, 0, 255)
INTR_SNAKE_COLOR = COLOR_BLUE

GAME_FRAME_RATE = 15

# Definitions for learning model
EMPTY_CELL_VALUE = 0
FOOD_CELL_VALUE = 1
SNAKE_BODY_CELL_VALUE = 2
SNAKE_HEAD_CELL_VALUE = 3


# VERSIONING
# FIXME: Figure out a way to automatically populate this
# from git tags.
VERSION_NUMBER = 0.1
