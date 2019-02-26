from graphics import *
from snake_game import *
import time
import operator
win = GraphWin("Snake Game", 700, 700)
win.setBackground('black')
game = SnakeGame(win)
# game.draw()
over = False
while not over:
    over = game.update()
    time.sleep(0.1)
