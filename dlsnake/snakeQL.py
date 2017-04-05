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
    numTrials = 1000
    i = 0
    weights = None
    while i < numTrials:
        ep = (numTrials - i) / numTrials
        al = (numTrials - i) / numTrials
        print(ep)
        gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                              foodAgent=MaxManhattanFoodAgent)
        if gui:
            guiDriver = toGUI(gameState, cfg.CELL_WIDTH, FRAME_RATE)
        agent = ApproxQAgent(alpha=0.009, gamma=0.99, epsilon=0.5,
                             featureExtractor=SimpleFeatureExtractor,
                             weights = weights)
        died = False
        gameState.setFoodScore(500)
        while not died and not quitGame:
            if enableGUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quitGame = True
                        break
            action = agent.getAction(gameState)
            print("action: ", action)
            currGameState = copy.deepcopy(gameState)
            gameState.chooseAction(action)
            gameState.executeAction()
            nextGameState = copy.deepcopy(gameState)
            reward = nextGameState.score - currGameState.score
            print(reward)
            agent.update(currGameState, action, reward, nextGameState)
            if enableGUI:
                guiDriver.show()
            if enableTextGraphics:
                print(gameState.getGrid())
                print()
            died = gameState.gameOver
            weights = agent.weights
            print(weights)
            # input('continue')
            # print('weights: ', agent.getWeights())
            input('Continue?')

        i += 1
        if i % 100 == 0:
            score = gameState.score
            snakeLen = len(gameState.snake.getSnakeCordinateList())
            print("Game Over!")
            print("\tScore: %d" % score)
            print("\tSnakeLen: %d" % snakeLen)
    if guiDriver is not None:
        pygame.quit()


if __name__ == '__main__':
    main()
