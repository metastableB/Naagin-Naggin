#
# @author:Don Dennis (metastableB)
# main.py
#

import os
import time
import dlsnake.config as cfg
import numpy as np
from dlsnake.learning.learnsnake import LearnSnake
from dlsnake.learning.learnfood import LearnFood


def main():
    screen_dim = (cfg.Y_MAX, cfg.X_MAX)
    # Fill with empty cell value
    screen_array = np.zeros(screen_dim)
    s = LearnSnake(5, 5)
    f = LearnFood()
    gameTime = 1000
    while gameTime:
        os.system('clear')
        prev_x, prev_y = s.get_head()
        prev_fx, prev_fy = f.get_food()
        #next_move = f()
        next_move = 'D'
        if next_move == 'U':
            s.direction(0, -1)
        if next_move == 'D':
            s.direction(0, 1)
        if next_move == 'L':
            s.direction(-1, 0)
        if next_move == 'R':
            s.direction(1, 0)
        s.update()
        if s.eat(f.x, f.y):
            f.new_food()
        s.show(screen_array)
        screen_array[prev_y][prev_x] = cfg.EMPTY_CELL_VALUE
        f.show(screen_array)
        screen_array[prev_fy][prev_fx] = cfg.EMPTY_CELL_VALUE
        print(screen_array)
        gameTime -= 1
        time.sleep(0.1)
    quit()


if __name__ == '__main__':
    main()
