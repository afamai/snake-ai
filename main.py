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
start = time.time()
g = Genome(3, 1)
g2 = Genome(3, 1)
end = time.time()
print('init time', end - start)
# g.mutate_add_node()
# g2.fitness_score = 2
# g3 = Genome.single_point_crossover(g, g2)
# print(g.input_nodes + g.hidden_nodes + g.output_nodes)
# print(g2.input_nodes + g2.hidden_nodes + g2.output_nodes)
# print(g3.input_nodes + g3.hidden_nodes + g3.output_nodes)
# print(g3.connections[0].in_node)
p = Population(10, 3, 1)
print(p.generate_new_generation())

keys = ['Up', 'Right', 'Down', 'Left']

win = GraphWin("Snake Game", 700, 700)
win.setBackground('black')
snake = Snake(5, 5, SnakeGame.RIGHT, 3)
board = Board(10, 10)
game = SnakeGame(win, snake, board)

# game loop
# over = False
# while not over:
#     data = np.array(board.data)
#     result = g.activate(data.flatten())
#     key = keys[np.argmax(result)]
#     over = game.update(key)
#     time.sleep(0.05)
