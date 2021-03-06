#
# @author:Don Dennis (metastableB)
# reflexAgent.py
#

import random
from dlsnake.agents.agent import Agent
from dlsnake.base.featureExtractor import SimpleFeatureExtractor4 as FeatureExtractor


class ReflexAgent(Agent):
    '''
    Reflex agent with different evaluation functions.
    A reflex agent chooses an action at each choice point
    by examining its alternatives via a state evaluation function.
    '''

    def __init__(self, agentId=0):
        self.agentId = agentId
        self.silent = False

    def getAction(self, gameState):
        """
        Iterates over all actions and returns the
        most optimun action depending on the evaluation
        function
        """
        legalMoves = gameState.getLegalActionsSnake()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[
            index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        if not self.silent:
            print("All scores: ", scores)
            print("chosing: " + str(legalMoves[chosenIndex]))
            print()
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        A simple evaluation function
        """
        successorGameState = currentGameState.generateSuccessor(
            action)
        value = 0.0
        newFood = successorGameState.getFoodCordinate()
        newPos = successorGameState.getSnakeHeadCordinate()
        newScore = successorGameState.getScore()
        oldScore = currentGameState.getScore()
        from dlsnake.base.util import manhattanDistance
        foodVicinityFactor = manhattanDistance(newPos, newFood)
        scoreFactor = newScore - oldScore
        if foodVicinityFactor != 0:
            value += 1.0 / foodVicinityFactor
        else:
            value += 1.0
        if scoreFactor != 0:
            value += scoreFactor

        # We don't obviously want to die
        if successorGameState.gameOver:
            value -= 10
        return value


class ReflexAgentControl(ReflexAgent):
    '''
    A control reflex agent used for comparison
    with Q-learning with approximation
    '''

    def __init__(self, agentId=0):
        self.agentId = agentId
        self.silent = True
        self.featExtractor = FeatureExtractor()
        self.weights = {}
        # for f in self.featExtractor.getFeatureKeys():
        #     self.weights[f] = random.uniform(0, 1)
        self.weights = {
            'Min Circular Food Vicinity': 5.0,
            'Collision Factor': -5.9,
            'Gradient Snake Vicinity': -1.2
        }

    def evaluationFunction(self, currentGameState, action):
        '''
        Uses the feature extractors evalution (LAF) function
        with custom weights to override the evaluationFunction
        '''
        features = self.featExtractor.getFeatures(currentGameState, action)
        v = 0.0
        for f in features:
            v += self.weights[f] * features[f]
        return v
