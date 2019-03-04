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
snake = Snake(12, 12, SnakeGame.RIGHT, 3)
board = Board(50, 50)
game = SnakeGame(win, snake, board)
g = Genome(2500, 4)
keys = ['Up', 'Right', 'Down', 'Left']
# game loop
over = False
print(Genome.innov_number)
g.mutate_add_node()
print(Genome.innov_number)
while not over:
    data = np.array(board.data)
    result = g.activate(data.flatten())
    key = keys[np.argmax(result)]
    over = game.update(key)
    time.sleep(0.05)
