#
# @author:Don Dennis (metastableB)
# gui_game.py
#

import time
from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
import dlsnake.config as cfg
from dlsnake.base.gameState import GameState
import pygame
from dlsnake.agents.reflexAgent import ReflexAgent
from dlsnake.agents.foodAgent import MaxManhattanFoodAgent

frameRate = cfg.GAME_FRAME_RATE


def playGameUser(gameState, gui, enableGUI=False):
    '''
    Runs a gui version of the agme that
    can be played using the arrow keys
    '''
    died = False
    while not died:
        eventList = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                died = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    eventList.append('UP')
                    # gameState.chooseAction('UP')
                if event.key == pygame.K_DOWN:
                    eventList.append('DOWN')
                    # gameState.chooseAction('DOWN')
                if event.key == pygame.K_LEFT:
                    eventList.append('LEFT')
                    # gameState.chooseAction('LEFT')
                if event.key == pygame.K_RIGHT:
                    eventList.append('RIGHT')
                    # gameState.chooseAction('RIGHT')

        if len(eventList) is not 0:
            gameState.chooseAction(eventList[-1])
        gameState.executeAction()
        gameState.update()
        died = gameState.gameOver
        if enableGUI:
            gui.show()
        else:
            print(gameState.getGrid())
            print()
    time.sleep(1)
    pygame.quit()
    quit()


def playGameAgent(gameState, gui, agent, enableGUI=False):
    '''
    Runs a gui version of the agme that
    can be played using the arrow keys
    '''
    died = False
    while not died:
        action = agent.getAction(gameState)
        gameState.chooseAction(action)
        gameState.executeAction()
        gameState.update()
        if enableGUI:
            gui.show()
        else:
            print(gameState.getGrid())
            print()

        gui.show()

    pygame.quit()
    quit()


def main():
    userPlayGame = False
    agentPlayGame = not userPlayGame
    enableGUI = True
    gs = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                   foodAgent=MaxManhattanFoodAgent)
    gui = toGUI(gs, cfg.CELL_WIDTH)
    if userPlayGame:
        playGameUser(gs, gui, enableGUI)
    elif agentPlayGame:
        reflexAgent = ReflexAgent()
        playGameAgent(gs, gui, reflexAgent, enableGUI)


if __name__ == '__main__':
    main()
