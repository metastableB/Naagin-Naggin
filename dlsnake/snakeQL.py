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

import time
import sys
import pprint
import math
import pygame
import copy
import dlsnake.config as cfg
from dlsnake.base.gameState import GameState
from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
from dlsnake.base.featureExtractor import SimpleFeatureExtractor2 as Neighbor
from dlsnake.agents.foodAgent import RandomFoodAgent
from dlsnake.agents.approxQAgent import ApproxQAgent
FRAME_RATE = cfg.GAME_FRAME_RATE
VERSION = cfg.VERSION_NUMBER


def main():
    silent = False
    enableGUI = True and not silent
    died = False
    quitGame = False
    enableTextGraphics = False
    enableTextGraphics = enableTextGraphics and not silent
    numTrials = 50000
    i = 0
    weights = None
    average_score = 0.0
    average_snake_len = 0.0
    while i < numTrials:
        ep = (numTrials - i) / numTrials
        gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                              foodAgent=RandomFoodAgent)
        if enableGUI:
            guiDriver = toGUI(gameState, cfg.CELL_WIDTH, FRAME_RATE)
        agent = ApproxQAgent(alpha=ep, gamma=0.90, epsilon=ep,
                             featureExtractor=Neighbor,
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
            reward = nextGameState.score - currGameState.score
            agent.update(currGameState, action, reward, nextGameState)
            if enableGUI:
                guiDriver.show()
            if enableTextGraphics:
                print(gameState.getGrid())
                print()
            died = gameState.gameOver
        i += 1
        average_score += gameState.score
        average_snake_len += len(gameState.getSnakeCordinates())
        if i % 1000 == 0:
            average_score /= 1000
            average_snake_len /= 1000
            print(i, "Episodes Played.")
            print("\tAverage Score: %d" % average_score)
            print("\tAverage SnakeLen: %d" % average_snake_len)
            print("\tEpsilon: ", ep)
            average_score = 0.0
            average_snake_len = 0.0
            pprint.pprint(weights)
            enableGUI = True

        else:
            enableGUI = False
        # Game Episode is over
        weights = agent.weights
        # a = weights['Occupied Factor']
        # b = weights['Simple Food Vicinity']
        # print("%f,%f" % (a, b))

    if enableGUI:
        pygame.quit()


if __name__ == '__main__':
    main()
