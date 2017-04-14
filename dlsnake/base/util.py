#
# @author:Don Dennis (metastableB)
# util.py
#
# Utility functions

from dlsnake.base import gameState

def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def circularManhattanDistance(snakePos, foodPos,
                              XY_MAX, direction):
    '''
    Returns manhattan distance when snake has to go to the
    border when travelling along direction
    '''
    if direction not in gameState.GameState.ALL_ACTIONS:
        raise ValueError("Invalid Direction Specified")

    sX, sY = snakePos
    X_MAX, Y_MAX = XY_MAX
    ret = None
    if direction == gameState.GameState.ACTION_UP:
        ret = sY + 1 + manhattanDistance(foodPos, (sX, Y_MAX))
    elif direction == gameState.GameState.ACTION_DOWN:
        ret = Y_MAX - sY + 1 + manhattanDistance(foodPos, (sX, 0))
    elif direction == gameState.GameState.ACTION_LEFT:
        ret = sX + 1 + manhattanDistance(foodPos, (X_MAX, sY))
    elif direction == gameState.GameState.ACTION_RIGHT:
        ret = X_MAX - sX + 1 + manhattanDistance(foodPos, (0, sY))
    return ret
