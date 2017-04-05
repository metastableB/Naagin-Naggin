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
    gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                          foodAgent=MaxManhattanFoodAgent)
    gui = True
    if gui:
        guiDriver = toGUI(gameState, cfg.CELL_WIDTH, FRAME_RATE)

    agent = ApproxQAgent(alpha=0.9, gamma=0.99, epsilon=0.5,
                         featureExtractor=SimpleFeatureExtractor)
    died = False
    quitGame = False
    silent = False
    enableTextGraphics = False
    enableGUI = gui is not None and not silent
    csvOut = False
    enableTextGraphics = enableTextGraphics and not silent
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
        agent.update(currGameState, action, reward, nextGameState)
        if enableGUI:
            guiDriver.show()
        if enableTextGraphics:
            print(gameState.getGrid())
            print()
        died = gameState.gameOver
        print('weights: ', agent.getWeights())

    score = gameState.score
    snakeLen = len(gameState.snake.getSnakeCordinateList())
    if not silent:
        print("Game Over!")
        print("Score: %d" % score)
        print("SnakeLen: %d" % snakeLen)
        time.sleep(2)
    if csvOut:
        print('%d, %d' % (score, snakeLen))
        import sys
        sys.stdout.flush()
    if guiDriver is not None:
        pygame.quit()


if __name__ == '__main__':
    main()
