#
# @author:Don Dennis (metastableB)
# approxQAgent.py
#
import random
from dlsnake.agents.agent import Agent


class approxQAgent(Agent):
    '''
    Approximate Q learning agent
    '''

    def __init__(self, **args):
        self.alpha = args['alpha']
        self.gamma = args['gamma']
        self.epsilon = args['epsilon']
        self.featExtractor = args['featureExtractor']
        self.weights = self.featExtractor.getWeightDict()

    def getAction(self, gameState, epsilon=0.0):
        """
        Returns the next action to take from the
        current state after looking at all q-states
        that follow.
        """
        legalMoves = gameState.getLegalActionsSnake()

        if not legalMoves:
            raise ValueError("There are no legal moves!" +
                             " How is this possible!")
        # Choose one of the best actions
        if random.uniform(0, epsilon):
            return random.choice(legalMoves)
        return self.computeActionFromQValues(gameState)

    def getQValue(self, gameState, action):
        features = self.featExtractor.getFeatures(gameState, action)
        q = 0.0
        for f in features:
            q += features[f] * self.weights[f]
        return q

    def compulteActionFromQValues(self, gameState):
        legalMoves = gameState.getLegalActions()
        if not legalMoves:
            # FIXME: Check for game over
            raise ValueError('No legal Actions!')
        qvalues = [self.getQValue(gameState, action) for action in legalMoves]
        maxq = max(qvalues)
        possibleMoves = []
        for action in legalMoves:
            if abs(self.getQValue(gameState, action) - maxq) <= 0.0000001:
                possibleMoves.append(action)
        return random.choice(possibleMoves)

    def computeValueFromQValues(self, gameState):
        values = []
        legalMoves = gameState.getLegalActions()
        if not legalMoves:
            raise ValueError('No legal Actions!')
        for action in legalMoves:
            q = self.getQValue(gameState, action)
            values.append(q)
        return max(values)

    def update(self, currGameState, action, nextGameState):
        gamma = self.gamma
        alpha = self.alpha
        reward = nextGameState['Score'] - currGameState['Score']
        difference = reward
        difference += gamma * self.computeValueFromQValues(nextGameState)
        features = self.featExtractor.getFeatures(currGameState, action)
        for f in features:
            self.weights[f] += alpha * difference * features[f]

    def getPolicy(self, gameStateRep):
        return self.compulteActionFromQValues(gameStateRep)

    def getValue(self, gameStateRep):
        return self.computeValueFromQValues(gameStateRep)
