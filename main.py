from graphics import *
from snake_game import *
from genome import *
from link import *
from node import *
import numpy as np
import time
import operator
win = GraphWin("Snake Game", 700, 700)
win.setBackground('black')

# init
snake = Snake(25, 25, SnakeGame.RIGHT, 3)
board = Board(50, 50)
game = SnakeGame(win, snake, board)
g = Genome(250, 4)
keys = ['Up', 'Right', 'Down', 'Left']
# game loop
over = False
while not over:
    data = np.array(board.data)
    result = g.activate(data.flatten())
    key = keys[np.argmax(result)]
    print(key)
    over = game.update(key)
    time.sleep(0.1)
