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
    FACTORS = [FOOD_VICINITY, SCORE_FACTOR]

    def __init__(self):
        self.featureKeys = self.FACTORS

    def getFeatures(self, gameState, action):
        successorGameState = gameState.generateSuccessor(action)
        foodPos = successorGameState.getFoodCordinate()
        snakePos = successorGameState.getSnakeHeadCordinate()
        from dlsnake.base.util import manhattanDistance
        foodVicinityFactor = manhattanDistance(foodPos, snakePos)
        foodVicinityFactor = 1 / foodVicinityFactor
        newScore = successorGameState.score
        return {self.FOOD_VICINITY: 0,
                self.SCORE_FACTOR: newScore}


if __name__ == '__main__':
    sfe = SimpleFeatureExtractor()
    print(dir(sfe))
