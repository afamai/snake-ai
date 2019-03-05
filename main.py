from graphics import *
from snake_game import *
from genome import *
from population import Population
from link import *
from node import *
import numpy as np
import time
import operator
import copy
# init
# start = time.time()
# p = Population(50, 2500, 4)
# end = time.time()
# print('init time', end - start)

keys = ['Up', 'Right', 'Down', 'Left']

win = GraphWin("Snake Game", 700, 700)
win.setBackground('black')
game = SnakeGame(10, 10, 5, 5, SnakeGame.RIGHT, win)

# game loop
over = False
step = 100
for i in range(10):
    game.update()
    print(game.to_string())
    time.sleep(1)
    # for g in p.genomes:
    #     for i in range(step):
    #         data = np.array(board.data)
    #         result = g.activate(data.flatten())
    #         key = keys[np.argmax(result)]
    #         over = game.update(key)
    #         if over:
    #             break
    #     g.fitness_score = game.point
    #     game.reset()
    
    # best = p.get_best()
    # # for i in range(step):
    # #     data = np.array(board.data)
    # #     result = g.activate(data.flatten())
    # #     key = keys[np.argmax(result)]
    # #     over = game.update(key)
    # #     if over:
    # #         break
    # #     time.sleep(0.01)
    # # game.reset()
    # p.generate_new_generation()
    
    # print(n+1, best.fitness_score)
    # if n % 5:
    #     step += 100

win.close()