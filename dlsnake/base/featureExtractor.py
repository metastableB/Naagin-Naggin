#
# @author:Don Dennis (metastableB)
# featureExtractor.py
#
import random
from dlsnake.base.util import manhattanDistance, circularManhattanDistance
from dlsnake.base.gameState import GameState


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
        self.getFeatureKeys = None
        self.scoreRange = None

    def getFeatures(self, gameState):
        pass

    def getReward(self, gameState, nextGameState):
        if self.scoreRange is None:
            scores = [gameState.foodScore]
            scores.append(gameState.livingScore)
            scores.append(gameState.completionScore)
            scores.append(gameState.collisionScore)
            scores.append(gameState.minAllowedScore)
            min_ = min(scores)
            max_ = max(scores)
            if min_ >= 0 or max_ <= 0:
                msg = "Minimum score and maximum score "
                msg += "should be on either side of 0"
                raise ValueError(msg)
            self.scoreRange = max_ - min_
        scoreDiff = nextGameState.score - gameState.score
        return scoreDiff / self.scoreRange

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
        self.scoreRange = None

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
    A very simple feature extractor for approx Q - learning.
    '''
    FOOD_VICINITY = 'Simple Food Vicinity'
    OCCUPIED = 'Occupied Factor'
    FACTORS = [FOOD_VICINITY, OCCUPIED]

    def __init__(self):
        self.scoreRange = None
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


class SimpleFeatureExtractor3(FeatureExtractor):
    '''
    A very simple feature extractor for approx Q - learning.
    '''
    CIRCULAR_FOOD_VICINITY = 'Min Circular Food Vicinity'
    GRAD_VICINITY = 'Gradient Snake Vicinity'
    COLLISION = 'Collision Factor'
    FACTORS = [CIRCULAR_FOOD_VICINITY, COLLISION]

    def __init__(self):
        self.scoreRange = None
        self.featureKeys = self.FACTORS
        self.X_MAX = None
        self.Y_MAX = None
        self.allDirections = GameState.ALL_ACTIONS

    def getFeatures(self, gameState, action):
        # We don't want new food as we want to detect
        # if the snake ate the food
        successorGameState = gameState.generateSuccessor(
            action, newFood = False)
        circularMD = self.getMinCircularManhattanDistance(successorGameState)
        if circularMD is None:
            circularMD = 1.1
        else:
            circularMD = 1.0 / float(circularMD)
        snakePos = successorGameState.getSnakeHeadCordinate()
        collision = 0.0
        if snakePos in gameState.getSnakeCordinates():
            collision = 1.3
        return {self.CIRCULAR_FOOD_VICINITY: circularMD,
                self.COLLISION: collision}

    def getMinCircularManhattanDistance(self, gameState):
        '''
        Returns the minimum circular manhattan distance.
        Where circular is defined as a motion through the
        ends of the grid (borders of the gird)
        '''
        md = []
        foodPos = gameState.getFoodCordinate()
        if None in foodPos:
            return None
        snakePos = gameState.getSnakeHeadCordinate()
        temp = manhattanDistance(snakePos, foodPos)
        md.append(temp)
        if self.X_MAX is None:
            self.X_MAX = gameState.numXCell - 1
            self.Y_MAX = gameState.numYCell - 1
        XY_MAX = (self.X_MAX, self.Y_MAX)
        # Moving Up
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_UP))
        # Moving into lower border
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_DOWN))
        # Moving into left border
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_LEFT))
        # Moving into right border
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_RIGHT))
        return min(md)


class SimpleFeatureExtractor4(FeatureExtractor):
    '''
    A very simple feature extractor for approx Q - learning.
    '''
    CIRCULAR_FOOD_VICINITY = 'Min Circular Food Vicinity'
    GRAD_VICINITY = 'Gradient Snake Vicinity'
    COLLISION = 'Collision Factor'
    FACTORS = [CIRCULAR_FOOD_VICINITY, COLLISION, GRAD_VICINITY]

    def __init__(self):
        self.scoreRange = None
        self.featureKeys = self.FACTORS
        self.X_MAX = None
        self.Y_MAX = None
        self.allDirections = GameState.ALL_ACTIONS

    def getFeatures(self, gameState, action):
        # We don't want new food as we want to detect
        # if the snake ate the food
        successorGameState = gameState.generateSuccessor(
            action, newFood = False)
        circularMD = self.getMinCircularManhattanDistance(successorGameState)
        if circularMD is None:
            circularMD = 1.1
        else:
            circularMD = 1.0 / float(circularMD)

        getGradVicinity = self.getGradVicinity(successorGameState)
        snakePos = successorGameState.getSnakeHeadCordinate()
        collision = 0.0
        if snakePos in gameState.getSnakeCordinates():
            collision = 1.3
        return {self.CIRCULAR_FOOD_VICINITY: circularMD,
                self.COLLISION: collision,
                self.GRAD_VICINITY: getGradVicinity}

    def getMinCircularManhattanDistance(self, gameState):
        '''
        Returns the minimum circular manhattan distance.
        Where circular is defined as a motion through the
        ends of the grid (borders of the gird)
        '''
        md = []
        foodPos = gameState.getFoodCordinate()
        if None in foodPos:
            return None
        snakePos = gameState.getSnakeHeadCordinate()
        temp = manhattanDistance(snakePos, foodPos)
        md.append(temp)
        if self.X_MAX is None:
            self.X_MAX = gameState.numXCell - 1
            self.Y_MAX = gameState.numYCell - 1
        XY_MAX = (self.X_MAX, self.Y_MAX)
        # Moving Up
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_UP))
        # Moving into lower border
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_DOWN))
        # Moving into left border
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_LEFT))
        # Moving into right border
        md.append(circularManhattanDistance(
            snakePos, foodPos, XY_MAX, GameState.ACTION_RIGHT))
        return min(md)

    def getGradVicinity(self, gameState):
        '''
        Returns a number indicating if we are moving
        away from the body of the snake or towards it.
        We calculate the negated inverse of the Manhattan
        distance of all points we are moving towards
        '''
        if self.X_MAX is None:
            self.X_MAX = gameState.numXCell - 1
            self.Y_MAX = gameState.numYCell - 1
        XY_MAX = (self.X_MAX, self.Y_MAX)
        direction = gameState.getCurrentDirection()
        snakePos = gameState.getSnakeHeadCordinate()
        allPos = gameState.getSnakeCordinates()
        allPos.remove(snakePos)
        ret = 0.0
        sX, sY = snakePos
        for pos in allPos:
            x, y = pos
            if direction == GameState.ACTION_RIGHT:
                if x > sX:
                    md = manhattanDistance((x, y), (sX, sY))
                    ret += 1 / md
                else:
                    md = circularManhattanDistance(snakePos, pos, XY_MAX,
                                                   GameState.ACTION_RIGHT)
                    ret += 1 / md
            elif direction == GameState.ACTION_LEFT:
                if x < sX:
                    md = manhattanDistance((x, y), (sX, sY))
                    ret += 1 / md
                else:
                    md = circularManhattanDistance(snakePos, pos, XY_MAX,
                                                   GameState.ACTION_LEFT)
                    ret += 1 / md
            elif direction == GameState.ACTION_UP:
                if y < sY:
                    md = manhattanDistance((x, y), (sX, sY))
                    ret += 1 / md
                else:
                    md = circularManhattanDistance(snakePos, pos, XY_MAX,
                                                   GameState.ACTION_UP)
                    ret += 1 / md
            else:
                if y > sY:
                    md = manhattanDistance((x, y), (sX, sY))
                    ret += 1 / md
                else:
                    md = circularManhattanDistance(snakePos, pos, XY_MAX,
                                                   GameState.ACTION_DOWN)
                    ret += 1 / md
        return ret


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
