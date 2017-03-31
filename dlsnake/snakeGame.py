#
# @author:Don Dennis (metastableB)
# gui_game.py
#

import time
import argparse
import pygame
from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
from dlsnake.base.gameState import GameState
from dlsnake.agents.reflexAgent import ReflexAgent
from dlsnake.agents.foodAgent import RandomFoodAgent, MaxManhattanFoodAgent
import dlsnake.config as cfg

FRAME_RATE = cfg.GAME_FRAME_RATE
VERSION = cfg.VERSION_NUMBER


def playGameUser(gameState, gui, enableText=False):
    '''
    Runs a gui version of the agme that
    can be played using the arrow keys
    '''
    died = False
    quitGame = False
    while not died and not quitGame:
        eventList = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame = True
                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    eventList.append('UP')
                if event.key == pygame.K_DOWN:
                    eventList.append('DOWN')
                if event.key == pygame.K_LEFT:
                    eventList.append('LEFT')
                if event.key == pygame.K_RIGHT:
                    eventList.append('RIGHT')

        if len(eventList) is not 0:
            gameState.chooseAction(eventList[-1])
        gameState.executeAction()
        gameState.update()
        died = gameState.gameOver
        gui.show()
        if enableText:
            print(gameState.getGrid())
            print()
    if not quitGame:
        time.sleep(1)
    pygame.quit()
    quit()


def playGameAgent(gameState, guiDriver, agent, enableText=False):
    '''
    Runs a gui version of the agme that
    can be played using the arrow keys
    '''
    died = False
    agent = agent()
    quitGame = False
    enableGUI = guiDriver is not None
    while not died and not quitGame:
        if enableGUI:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame = True
                    break
        action = agent.getAction(gameState)
        gameState.chooseAction(action)
        gameState.executeAction()
        gameState.update()
        if enableGUI:
            guiDriver.show()
        if enableText:
            print(gameState.getGrid())
            print()
        died = gameState.gameOver
    print("Game Over!")
    score = gameState.score
    snakeLen = len(gameState.snake.getSnakeCordinateList())
    print("Score: %d" % score)
    print("SnakeLen: %d" % snakeLen)
    pygame.quit()
    quit()


class ArgumentOptions:
    agentChoiceDict = {
        'ReflexAgent': ReflexAgent
    }
    agentChoices = agentChoiceDict.keys()
    foodAgentChoiceDict = {
        'RandomFoodAgent': RandomFoodAgent,
        'MaxManhattanFoodAgnet': MaxManhattanFoodAgent
    }
    foodAgentChoices = foodAgentChoiceDict.keys()


def get_arguments():
    descr = '''
    Naagin-Nagging v''' + str(VERSION) + '''
    - Applying Deep Q-Learning to Snake.
    '''
    ap = argparse.ArgumentParser(description=descr)
    agentChoices = ArgumentOptions.agentChoices
    ap.add_argument('-a', '--agent',
                    help="Specify the agent to use for playing snake.",
                    default=None,
                    choices=agentChoices,
                    dest='agent')
    foodAgentChoices = ArgumentOptions.foodAgentChoices
    ap.add_argument('-s', '--food-agent',
                    help="Specify the food agent to use.",
                    default='RandomFoodAgent',
                    choices=foodAgentChoices,
                    dest='foodAgent')
    ap.add_argument('-n', '--no-graphics',
                    help="Disable graphics and run silently.",
                    action='store_true',
                    default=False,
                    dest='noGraphics')
    ap.add_argument('-t', '--text-graphics',
                    help="Enable text graphics.",
                    action='store_true',
                    default=False,
                    dest='textGraphics')
    ap.add_argument('-f', '--frame-rate',
                    help='Frame rate for GUI graphics.',
                    action='store',
                    dest='frameRate',
                    type=int,
                    default=FRAME_RATE)
    args = ap.parse_args()
    return args


def main():
    args = get_arguments()
    foodAgent = args.foodAgent
    foodAgent = ArgumentOptions.foodAgentChoiceDict[foodAgent]
    snakeAgent = args.agent
    if snakeAgent is not None:
        snakeAgent = ArgumentOptions.agentChoiceDict[snakeAgent]
    enableGUI = not args.noGraphics
    enableText = args.textGraphics
    frameRate = args.frameRate
    gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                          foodAgent=foodAgent)
    guiDriver = None
    if enableGUI:
        guiDriver = toGUI(gameState, cfg.CELL_WIDTH, frameRate)

    if snakeAgent is None:
        if guiDriver is None:
            print("Error: Graphics disabled and interactive game requested.")
            print("You have turned off graphics. " +
                  "Either turn graphics on or specify an automated agent.")
            exit(1)
        playGameUser(gameState, guiDriver, enableText)
    else:
        playGameAgent(gameState, guiDriver, snakeAgent, enableText)


if __name__ == '__main__':
    main()
