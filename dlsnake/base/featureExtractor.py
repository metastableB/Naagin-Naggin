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
    SCORE_FACTOR = 'Score Factor'
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


if __name__ == '__main__':
    sfe = SimpleFeatureExtractor()
    print(dir(sfe))
