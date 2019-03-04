from graphics import *
from snake_game import *
from genome import *
from link import *
from node import *
import numpy as np
import time
import operator
# init
start = time.time()
g = Genome(2500, 4)
end = time.time()
print('init time', end - start)

keys = ['Up', 'Right', 'Down', 'Left']

win = GraphWin("Snake Game", 700, 700)
win.setBackground('black')
snake = Snake(12, 12, SnakeGame.RIGHT, 3)
board = Board(50, 50)
game = SnakeGame(win, snake, board)

# game loop
over = False
while not over:
    data = np.array(board.data)
    result = g.activate(data.flatten())
    key = keys[np.argmax(result)]
    over = game.update(key)
    time.sleep(0.05)
