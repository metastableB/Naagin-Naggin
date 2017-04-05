#
# @author:Don Dennis (metastableB)
# agent.py
#


class Agent:
    '''
    Base class for all agents controlling snake. All
    agents must define the getAction() method.
    '''

    def __init__(self):
        pass

    def getAction(self, state):
        '''
        The agent will get a gamestate object and must
        return a action among the valid actions for the game
        '''
        pass

    def update(self, state, action, reward, nextState):
        '''
        Used for Q-learning and approximate q-learning
        based agents, wherein after each action, we have
        to update the internal weights as well
        Call this method after each move of game state.
        THERE IS NO WAY YET TO VALIDATE IF THIS METHOD
        IS BEING CALLED PROPERLY AND THE ONUS TO DO THAT
        IS ON THE USER.
        '''
        pass
