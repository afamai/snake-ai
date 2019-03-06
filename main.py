from graphics import GraphWin
from game import Game
from snake import Snake
import time
win = GraphWin('Snake Game', 700, 700)
win.setBackground('black')
snake = Snake(5, 5, Game.RIGHT, 3)
game = Game(10, 10, win)
game.start(snake)
while not game.over:
    game.update()
    print(game)
    time.sleep(1)
win.close()