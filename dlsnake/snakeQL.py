#
# @author:Don Dennis (metastableB)
# snakeQL.py
#
# FIXME: Merge snakeQL and snakeGame.py
# This is just lazy coding!
#
# @author:Don Dennis (metastableB)
# gui_game.py
#

import pygame
import copy
import dlsnake.config as cfg
from dlsnake.base.gameState import GameState
from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
from dlsnake.base.featureExtractor import SimpleFeatureExtractor4 as featExtractor
from dlsnake.agents.foodAgent import RandomFoodAgent
from dlsnake.agents.approxQAgent import ApproxQAgent
FRAME_RATE = cfg.GAME_FRAME_RATE
VERSION = cfg.VERSION_NUMBER


def main():
    # BEGIN Configuration Options
    enableGUI = False
    enableTextGraphics = False
    numTrials = 2000
    trainRange = numTrials * 0.80
    guiRange = 100
    weights = None
    average_score = 0.0
    average_snake_len = 0.0
    csv = True
    noUpdate = False
    # END COFIGURATION OPTIONS
    i = 0
    header = "Episode,Score,Length,Epsilon,Alpha"
    died = False
    quitGame = False
    for f in featExtractor().getFeatureKeys():
        temp = ',' + f
        header += temp
    if csv:
        print(header)
    while i < numTrials:
        if i < trainRange:
            ep = (numTrials - i) / numTrials
            al = ep*0.8
        else:
            ep = 0.01
            al = 0.01
        gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                              foodAgent=RandomFoodAgent)
        if enableGUI:
            guiDriver = toGUI(gameState, cfg.CELL_WIDTH, FRAME_RATE)
        agent = ApproxQAgent(alpha=al, gamma=0.700, epsilon=ep,
                             featureExtractor=featExtractor,
                             weights = weights)
        died = False
        while not died and not quitGame:
            if enableGUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quitGame = True
                        break
            action = agent.getAction(gameState)
            currGameState = copy.deepcopy(gameState)
            gameState.chooseAction(action)
            gameState.executeAction()
            nextGameState = copy.deepcopy(gameState)
            if not noUpdate:
                agent.update(currGameState, action, nextGameState)
            if enableGUI:
                guiDriver.show()
            if enableTextGraphics:
                print(gameState.getGrid())
                print()
            died = gameState.gameOver
        i += 1
        average_score += gameState.score
        average_snake_len += len(gameState.getSnakeCordinates())
        if not csv and i % guiRange == 0 and guiRange > 0:
            average_score /= guiRange
            average_snake_len /= guiRange
            print(i, "Episodes Played.")
            print("\tAverage Score: %f" % average_score)
            print("\tAverage SnakeLen: %f" % average_snake_len)
            print("\tEpsilon: ", ep)
            print("\tAlpha: ", al)
            print(weights)
            average_score = 0.0
            average_snake_len = 0.0
            enableGUI = True

        else:
            enableGUI = False
        # Game Episode is over
        weights = agent.weights
        if csv:
            episode = i
            score = gameState.score
            length = len(gameState.getSnakeCordinates())
            epsilon = ep
            alpha = al
            temp = "%d, %f, %f, %f, %f" % (
                episode, score, length, epsilon, alpha)
            for f in featExtractor().getFeatureKeys():
                temp += ', %f' % (agent.weights[f])
            print(temp)

    if enableGUI:
        pygame.quit()


if __name__ == '__main__':
    main()
