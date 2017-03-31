#
# @author:Don Dennis (metastableB)
# snake.py
#


class Snake():

    def __init__(self, x, y, numXCell, numYCell, growing = True):
        '''
        Initializes a snake to x,y position(cordinates). Positive x along
        width and positive y along top-down direction

        :param: numXCell: Number of cells in x direction
        :param: numYCell: Number of cells in y direction
        '''
        self.X_MAX = numXCell
        self.Y_MAX = numYCell
        self.X_MIN = 0
        self.Y_MIN = 0
        self.head = (x, y)
        self.previousTail = (None, None)
        self.cordinates = [self.head]
        # Moving towards right
        self.xspeed = 1
        self.yspeed = 0
        self.died = False
        self.growingSnake = growing

    def update(self):
        '''
        Updates the state of the snake and returns True if
        an update was successful. An update fails only when the
        snake is dead and the update is called.
        '''
        if self.died:
            return False
        x, y = self.head
        x += self.xspeed
        y += self.yspeed
        if x >= self.X_MAX:
            x = self.X_MIN
        if x < self.X_MIN:
            x = self.X_MAX - 1
        if y >= self.Y_MAX:
            y = self.Y_MIN
        if y < self.Y_MIN:
            y = self.Y_MAX - 1

        newHead = (x, y)
        if newHead in self.cordinates[1:]:
            self.died = True
            return False
        self.head = newHead
        self.previousTail = self.cordinates[-1]
        self.cordinates = self.cordinates[:-1]
        self.cordinates.insert(0, self.head)

        return True

    def direction(self, xsp, ysp):
        '''
        Updates the xspped anc yspeed. At least one among
        them should be zero all the time
        '''
        self.xspeed = xsp
        self.yspeed = ysp

    def eat(self, f_x, f_y):
        '''
        Returns True if the snake eats the food. Cordinates
        of the food are arguments. If `growingSnake` is set
        to true, the self.previousTail is used to increase the
        length of the snake. Hence after each self.update(),
        always call self.eat()
        '''
        x, y = self.head
        if (f_x is not x) or (f_y is not y):
            return False
        if self.growingSnake:
            self.cordinates.append(self.previousTail)
        return True

    def show(self, x, y):
        '''
        This function is to be called to show the snake.
        Exactly how show is defined depends on the environment
        using it
        Override if necessary
        '''
        pass

    def getHead(self):
        return self.head

    def getSnakeCordinateList(self):
        return self.cordinates

    def getCurrentDirection(self):
        return self.xspeed, self.yspeed

    def getSnakeLength(self):
        return len(self.cordinates)
