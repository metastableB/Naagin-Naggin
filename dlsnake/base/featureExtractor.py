#
# @author:Don Dennis (metastableB)
# featureExtractor.py
#
import random


class FeatureExtractor():
    '''
    Extractor features from the current gameState
    using the getFeatures method.

    Exposes:
    getFeatureKeys(): Returns list of string keys to the features
        extracted.
    getFeatures(gameState): Returns a dict of {featueKey:value}

    '''

    def __init__(self):
        pass

    def getFeatures(self, gameState):
        pass

    def getFeatureKeys(self):
        return self.featureKeys


class SimpleFeatureExtractor(FeatureExtractor):
    '''
    A very simple feature extractor for approx Q-learning.
    '''
    FOOD_VICINITY = 'Simple Food Vicinity'
    FACTORS = [FOOD_VICINITY]

    def __init__(self):
        self.featureKeys = self.FACTORS

    def getFeatures(self, gameState, action):
        # We don't want new food as we want to detect
        # if the snake ate the food
        successorGameState = gameState.generateSuccessor(
            action, newFood = False)
        foodPos = successorGameState.getFoodCordinate()
        if None in foodPos:
            return {self.FOOD_VICINITY: 2.0}
        snakePos = successorGameState.getSnakeHeadCordinate()
        from dlsnake.base.util import manhattanDistance
        foodVicinityFactor = manhattanDistance(foodPos, snakePos)
        foodVicinityFactor = 1 / foodVicinityFactor
        return {self.FOOD_VICINITY: foodVicinityFactor}


class SimpleFeatureExtractor2(FeatureExtractor):
    '''
    A very simple feature extractor for approx Q-learning.
    '''
    FOOD_VICINITY = 'Simple Food Vicinity'
    OCCUPIED = 'Occupied Factor'
    FACTORS = [FOOD_VICINITY, OCCUPIED]

    def __init__(self):
        self.featureKeys = self.FACTORS

    def getFeatures(self, gameState, action):
        # We don't want new food as we want to detect
        # if the snake ate the food
        successorGameState = gameState.generateSuccessor(
            action, newFood = False)
        foodPos = successorGameState.getFoodCordinate()
        if None in foodPos:
            return {self.FOOD_VICINITY: 2.0,
                    self.OCCUPIED: 0.0}
        snakePos = successorGameState.getSnakeHeadCordinate()
        from dlsnake.base.util import manhattanDistance
        foodVicinityFactor = manhattanDistance(foodPos, snakePos)
        foodVicinityFactor = 1.0 / foodVicinityFactor
        occupiedFactor = 0.0
        if snakePos in gameState.getSnakeCordinates():
            occupiedFactor = 1.0

        return {self.FOOD_VICINITY: foodVicinityFactor,
                self.OCCUPIED: occupiedFactor}


class OneNearestNeighbourFeatureExtractor(FeatureExtractor):
    '''
    Considers food vicinity and checks neighbors of head
    for collisions into snake body
    '''
    FOOD_VICINITY = 'Simple Food Vicinity'
    ONE_NEAREST_NEIGHBOURS = 'One-Nearest Neighbor'
    SCORE_LOST = 'Score Lost Factor'
    LENGTH = 'Length Factor'
    COMB_LENGTH_NEIGHBOUR = 'f(length, neighbor)'
    FACTORS = [FOOD_VICINITY]

    def __init__(self):
        self.featureKeys = self.FACTORS

    def getFeatures(self, gameState, action):
        # We don't want new food as we want to detect
        # if the snake ate the food
        successorGameState = gameState.generateSuccessor(
            action, newFood = False)
        foodPos = successorGameState.getFoodCordinate()
        if None in foodPos:
            foodVicinityFactor = 2.0
        else:
            snakePos = successorGameState.getSnakeHeadCordinate()
            from dlsnake.base.util import manhattanDistance
            foodVicinityFactor = manhattanDistance(foodPos, snakePos)
            foodVicinityFactor = 1 / foodVicinityFactor
        # Factor in the number of cells of the neighbor that
        # are parts of the snake.
        neighborCellCords = self.__getNeighborCellCords(successorGameState)
        snakeCords = gameState.getSnakeCordinates()
        oneNearestFactor = 0.0
        newHead = successorGameState.getSnakeHeadCordinate()
        # Detects if the new game state results in a crash
        neighborCellCords.append(newHead)
        for p in neighborCellCords:
            if p in snakeCords:
                oneNearestFactor -= 1.0
        # How much score did we loose/gain (-1 to 1)
        oldScore = gameState.score
        newScore = successorGameState.score
        scoreLostFactor = (newScore - oldScore)
        # Can happen if gameOVer
        if scoreLostFactor != 0:
            scoreLostFactor = 1 / scoreLostFactor
        # Length Factor
        length = len(successorGameState.getSnakeCordinates())
        length = 1 / length
        comb = length * oneNearestFactor
        return {self.FOOD_VICINITY: foodVicinityFactor
                # self.ONE_NEAREST_NEIGHBOURS: oneNearestFactor,
                # self.SCORE_LOST: scoreLostFactor,
                # self.LENGTH: length,
                # self.COMB_LENGTH_NEIGHBOUR: comb
                }

    def __getNeighborCellCords(self, gameState):
        x, y = gameState.getSnakeHeadCordinate()
        X_MAX = gameState.numXCell
        Y_MAX = gameState.numYCell
        cl = []
        x_ = (x + 1) % X_MAX
        y_ = (y + 1) % Y_MAX
        cl.append((x_, y))
        cl.append((x, y_))
        x_ = x - 1
        if x_ < 0:
            x_ = X_MAX - 1
        y_ = y - 1
        if y_ < 0:
            y_ = Y_MAX - 1
        cl.append((x_, y))
        cl.append((x, y_))
        return cl


if __name__ == '__main__':
    sfe = SimpleFeatureExtractor()
    print(dir(sfe))
