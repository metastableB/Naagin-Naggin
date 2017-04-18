#
# @author:Don Dennis (metastableB)
# gui_game.py
#

import time
import argparse
import pygame
from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
from dlsnake.base.gameState import GameState
from dlsnake.agents.reflexAgent import ReflexAgent, ReflexAgentControl
from dlsnake.agents.minMaxAgent import MinMaxAgent
from dlsnake.agents.foodAgent import RandomFoodAgent, MaxManhattanFoodAgent
import dlsnake.config as cfg
import multiprocessing

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
        died = gameState.gameOver
        gui.show()
        if enableText:
            print(gameState.getGrid())
            print()
    if not quitGame:
        time.sleep(1)
    pygame.quit()


def playGameAgent(gameState, guiDriver, agent,
                  enableTextGraphics=False,
                  silent=False,
                  csvOut=False):
    '''
    Runs a gui version of the agme that
    can be played using the arrow keys
    '''
    died = False
    quitGame = False
    enableGUI = guiDriver is not None and not silent
    enableTextGraphics = enableTextGraphics and not silent
    while not died and not quitGame:
        if enableGUI:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame = True
                    break
        action = agent.getAction(gameState)
        gameState.chooseAction(action)
        gameState.executeAction()
        if enableGUI:
            guiDriver.show()
        if enableTextGraphics:
            print(gameState.getGrid())
            print()
        died = gameState.gameOver

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


class ArgumentOptions:
    agentChoiceDict = {
        'ReflexAgent': ReflexAgent,
        'MinMaxAgent': MinMaxAgent,
        'ControlReflexAgent': ReflexAgentControl,
    }
    agentChoices = agentChoiceDict.keys()
    foodAgentChoiceDict = {
        'RandomFoodAgent': RandomFoodAgent,
        'MaxManhattanFoodAgent': MaxManhattanFoodAgent
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
                    help='Frame rate for GUI graphics. ' +
                    'Should be a non-zero integer.',
                    action='store',
                    dest='frameRate',
                    type=int,
                    default=FRAME_RATE)
    ap.add_argument('-z', '--silent',
                    help='Silently execute, no output to console' +
                    ' and no graphics.',
                    action='store_true',
                    default=False,
                    dest='silent')
    ap.add_argument('-m', '--simulate',
                    help='Run specified number of simulations on ' +
                    'each thread and ' +
                    'echo output (length, score) to console. Can be' +
                    ' multi-threaded using --thread',
                    default=0,
                    dest='simulate',
                    action='store',
                    type=int)
    ap.add_argument('-y', '--num-threads',
                    help='Specify the number of threads to use when' +
                    ' in simulation mode.',
                    default=1,
                    dest='num_threads',
                    action='store',
                    type=int)
    ap.add_argument('-d', '--depth',
                    help='Depth for searching. Only valid for MinMaxAgent.',
                    default=1,
                    type=int,
                    dest='depth')
    ap.add_argument('-c', '--csv',
                    help='Echo output in CSV format (length, score).',
                    default=False,
                    dest='csv',
                    action='store_true')
    args = ap.parse_args()
    return args


def run(args):
    '''
    Runs a single instance of the game. This is a conjugate
    to the simulate(args) method which (can) run multiple threaded
    instances of the game and echo outputs to console.
    '''
    foodAgent = args.foodAgent
    foodAgent = ArgumentOptions.foodAgentChoiceDict[foodAgent]
    snakeAgent = args.agent
    if snakeAgent is not None:
        snakeAgent = ArgumentOptions.agentChoiceDict[snakeAgent]
        snakeAgent = snakeAgent()
        snakeAgent.depth = args.depth
    enableGUI = not args.noGraphics
    enableTextGraphics = args.textGraphics
    silent = False
    if args.silent:
        enableGUI = False
        enableTextGraphics = False
        silent = True
    csvOut = args.csv
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
        playGameUser(gameState, guiDriver, enableTextGraphics)
    else:
        playGameAgent(gameState, guiDriver, snakeAgent,
                      enableTextGraphics, silent,
                      csvOut = csvOut)


def simulate(args):
    '''
    Run multiple threads of the game and echo output
    to console. FIXME: run and simulate can be merged,
    run() is just the base case for simulate.
    '''
    # Run N number of threads
    # and simulate K times on each thread
    numRuns = args.simulate
    while numRuns > 0:
        foodAgent = args.foodAgent
        foodAgent = ArgumentOptions.foodAgentChoiceDict[foodAgent]
        snakeAgent = args.agent
        if snakeAgent is not None:
            snakeAgent = ArgumentOptions.agentChoiceDict[snakeAgent]
            snakeAgent = snakeAgent()
            snakeAgent.depth = args.depth
        enableTextGraphics = False
        silent = True
        csvOut = True
        gameState = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL,
                              foodAgent=foodAgent)
        playGameAgent(gameState, None, snakeAgent,
                      enableTextGraphics, silent,
                      csvOut = csvOut)
        numRuns -= 1


def main():
    args = get_arguments()
    if args.simulate == 0:
        run(args)
    else:
        # We thread
        numThreads = args.num_threads
        jobs = []
        for i in range(0, numThreads):
            process = multiprocessing.Process(target=simulate, args=(args,))
            jobs.append(process)
        # Start simulations
        for job in jobs:
            job.start()

        # Make sure all runs have finished
        for job in jobs:
            job.join()
        # Done


if __name__ == '__main__':
    main()
