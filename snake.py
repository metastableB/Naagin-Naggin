#
# @author:Don Dennis (metastableB)
# snake.py
#


class Snake():
    # Grid of 10x10
    X_MAX = 10
    Y_MAX = 10
    X_MIN = 0
    Y_MIN = 0

    def __init__(self, x, y):
        self.x = 0
        self.y = 0
        self.score = 0
        # Value by which score should increment
        self.score_incr = 10
        # Moving towards right
        self.xpeed = 1
        self.yspeed = 0
        self.died = False

    def update(self):
        '''
        Updates the state of the snake and returns True if
        an update was successful. An update fails only when the
        snake is dead and the update is called.
        '''
        if self.died:
            return False
        x = self.x + self.xspeed
        y = self.y + self.yspeed
        if x >= self.X_MAX:
            x = self.X_MIN
        if y < self.X_MIN:
            x = self.X_MAX - 1
        if y >= self.Y_MAX:
            y = self.Y_MIN
        if y < self.Y_MIN:
            y = self.Y_MAX - 1
        self.x = x
        self.y = y

    def direction(self, xsp, ysp):
        '''
        Updates the xspped anc yspeed. At least one among
        them should be zero all the time
        '''
        self.xspeed = xsp
        self.yspped = ysp

    def eat(self, f_x, f_y):
        '''
        Returns True if the snake eats the food. Cordinates
        of the food are arguments
        '''
        if (f_x is not self.x) or (f_y is not self.y):
            return False
        self.score += self.score_incr
        return True

    def show(self, x, y):
        '''
        This function is to be called to show the snake.
        Exactly how show is defined depends on the environment
        using it
        Override if necessary
        '''