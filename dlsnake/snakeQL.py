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
import math
import pygame
import copy
import dlsnake.config as cfg
from dlsnake.base.gameState import GameState
from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
from dlsnake.base.featureExtractor import SimpleFeatureExtractor
from dlsnake.agents.foodAgent import MaxManhattanFoodAgent
from dlsnake.agents.approxQAgent import ApproxQAgent
FRAME_RATE = cfg.GAME_FRAME_RATE
VERSION = cfg.VERSION_NUMBER


def main():
    gui = True
    died = False
    quitGame = False
    silent = False
    enableTextGraphics = False
    enableGUI = gui and not silent
    enableTextGraphics = enableTextGraphics and not silent
    numTrials = 10
    i = 0
    weights = None
    average_score = 0.0
    average_snake_len = 0.0
    while i < numTrials:
        gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                              foodAgent=MaxManhattanFoodAgent)
        if gui:
            guiDriver = toGUI(gameState, cfg.CELL_WIDTH, FRAME_RATE)
        agent = ApproxQAgent(alpha=0.8, gamma=1.0, epsilon=0.0,
                             featureExtractor=SimpleFeatureExtractor,
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
        if i % 100 == 0:
            average_score /= 100
            average_snake_len /= 100
            print(i, " Episodes Played.")
            print("\tAverage Score: %d" % average_score)
            print("\tAverage SnakeLen: %d" % average_snake_len)
            average_score = 0.0
            average_snake_len = 0.0
            print("\t Weights: ", weights)

        # Game Episode is over
        weights = agent.weights

    if enableGUI:
        pygame.quit()


if __name__ == '__main__':
    main()
