#
# @author:Don Dennis (metastableB)
# gui_game.py
#


from dlsnake.base.gameStateToGUI import GameStateToGUI as toGUI
import dlsnake.config as cfg
from dlsnake.base.gameState import GameState
import pygame

frameRate = cfg.GAME_FRAME_RATE


def main():
    died = False
    gs = GameState(cfg.NUM_X_CELL, cfg.NUM_Y_CELL)
    gui = toGUI(gs, 50)
    while not died:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                died = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    gs.chooseAction('UP')
                if event.key == pygame.K_DOWN:
                    gs.chooseAction('DOWN')
                if event.key == pygame.K_LEFT:
                    gs.chooseAction('LEFT')
                if event.key == pygame.K_RIGHT:
                    gs.chooseAction('RIGHT')

        gs.executeAction()
        gs.update()

        # print(gs.getGrid())
        # print()

        gui.show()

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
