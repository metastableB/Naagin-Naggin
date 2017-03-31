#
# @author:Don Dennis (metastableB)
# minMaxAgent.py
#

from dlsnake.agents.agent import Agent


class MinMaxAgent(Agent):
    '''
    Reflex agent with based on minMax search. Searches uphill
    depth d as specified and returns the best course of action.
    Note that the number of stages to search blow out of proportion
    really quickly and hence a MinMax agent is not really useful.
    For example, with 10x10 grids, there are close to 100 places
    where the food can be placed and hence 100 legal moves for a random
    agent just at level 1.

    A ply of the tree comprises of one snake move followed by one
    move by the foodAgent. Hence depth=2 means that the snake
    and foodAgent gets to make exactly two moves each.
    '''

    def __init__(self, depth=1):
        self.depth = depth

    def getAction(self, gameState):
        """
        Iterates over all actions and returns the
        most optimum action depending on the evaluation
        function
        """
        agent = 0
        currentDepth = 1
        legalMoves = gameState.getLegalSnakeActions()
        max_val = float('-int')
        max_action = None
        for action in legalMoves:
            successorGameState = gameState.generateSnakeSuccessor(action)
            v = self.getMin(successorGameState, currentDepth, agent)
            if v > max_val:
                max_action = action
                max_val = v
        return max_action

    def getMin(self, gameState, currentDepth, foodAgent):
        if foodAgent == 0:
            raise ValueError("Agent 0 in min layer!")

        if gameState.gameOver or currentDepth > self.depth:
            return self.evaluationFunction(gameState)
        min_val = float('inf')
        legalMoves = gameState.getLegalActionsFoodAgent()
        for action in legalMoves:
            successorGameState = gameState.generateFoodAgentSuccessor(action)
            v = self.getMax(successorGameState, currentDepth + 1, 0)
            if v < min_val:
                min_val = v
        return min_val

    def getMax(self, gameState, currentDepth, agent):
        if agent != 0:
            raise ValueError("Agent is non-zero in max layer!")

        if gameState.gameOver or currentDepth > self.depth:
            return self.evaluationFunction(gameState)
        max_val = float('-inf')
        legalMoves = gameState.getLegalSnakeActions()
        for action in legalMoves:
            successorGameState = gameState.generateSnakeSuccessor(action)
            v = self.getMin(successorGameState, currentDepth, 1)
            if v > max_val:
                max_val = v
        return max_val

    def evaluationFunction(self, currentGameState, action):
        """
        A simple evaluation function
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generateSnakeSuccessor(
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
