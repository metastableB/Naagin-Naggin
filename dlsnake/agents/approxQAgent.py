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

    def __init__(self, agentId=0):
        self.agentId = agentId
        self.silent = True

    def getAction(self, gameStateRep, epsilon=0.0):
        """
        Returns the next action to take from the
        current state after looking at all q-states
        that follow.
        """
        legalMoves = gameStateRep.getLegalActionsSnake()

        if not legalMoves:
            raise ValueError("There are no legal moves!" +
                             " How is this possible!")
        # Choose one of the best actions
        if random.uniform(0, epsilon):
            return random.choice(legalMoves)
        return self.computeActionFromQValues(gameStateRep)

    def compulteActionFromQValues(self, gameStateRep):
        pass

    def getQValue(self, gameStateRep, action):
        pass

    def computeValueFromQValues(self, gameStateRep):
        pass

    def computeActionFromQValues(self, gameStateRep):
        pass

    def update(self, currGameStateRep, action, nextGameStateRep):
        pass

    def getPolicy(self, gameStateRep):
        return self.compulteActionFromQValues(gameStateRep)

    def getValue(self, gameStateRep):
        return self.computeValueFromQValues(gameStateRep)
