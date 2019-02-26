from graphics import *
from snake_game import *
import time
import operator
win = GraphWin("Snake Game", 700, 700)
win.setBackground('black')

# init
snake = Snake(3, 3, SnakeGame.RIGHT, 3)
board = Board(10, 10)
game = SnakeGame(win, snake, board)

# game loop
over = False
while not over:
    over = game.update()
    time.sleep(0.1)
