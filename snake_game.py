from graphics import GraphWin, Rectangle, Point
from msvcrt import getch
import numpy as np
import operator
import random
class SnakeGame:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    def __init__(self, width, height, start_x, start_y, direction, window):
        # create snake
        self.snake = []
        self.direction = direction
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        for i in range(3):
            self.snake.append((start_x + i * -direction[0], start_y + i * -direction[1]))
        
        # create board
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.window = window

        self.cell_width = window.getWidth() / width
        self.cell_height = window.getHeight() / height

        # draw the snake
        self.snake_rects = []
        for (x, y) in self.snake:
            self.board[y][x] = 1
            rect = self._draw_rect(x, y, 'white')
            self.snake_rects.append(rect)
        
        self.food = self.generate_new_food()
        self.point = 0
    
    def reset(self):
        self.point = 0
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

        # reset the snake
        while len(self.snake_rects) > 0:
            rect = self.snake_rects.pop()
            rect.setFill('black')
        
        self.snake = []
        for i in range(3):
            self.snake.append((self.start_x + i * -self.direction[0], self.start_y + i * -self.direction[1]))

        # draw the snake
        self.snake_rects = []
        for (x, y) in self.snake:
            self.board[y][x] = 1
            rect = self._draw_rect(x, y, 'white')
            self.snake_rects.append(rect)

        # generate new food
        self._draw_rect(self.food[0], self.food[1], 'black')
        self.food = self.generate_new_food()



    def update(self, key):
        # key = self.window.checkKey()
        if (key == 'Up' and self.direction != self.DOWN):
            self.direction = self.UP
        elif (key == 'Down' and self.direction != self.UP):
            print('down')
            self.direction = self.DOWN
        elif (key == 'Right' and self.direction != self.LEFT):
            self.direction = self.RIGHT
        elif (key == 'Left' and self.direction != self.RIGHT):
            self.direction = self.LEFT
        
        # move the snake
        new_pos = tuple(map(operator.add, self.snake[0], self.direction))
        
        # check if the snake is in the zone or dead
        if (new_pos in self.snake[1:] or self.outside_board(new_pos[0], new_pos[1])):
            return True
        
        self.snake.insert(0, new_pos)

        # draw the new head
        self.board[new_pos[1]][new_pos[0]] =  1
        head = self._draw_rect(new_pos[0], new_pos[1], 'white')
        self.snake_rects.insert(0, head)

        if new_pos == self.food:
            self.point += 1
            self.food = self.generate_new_food()
        else:
            # clear the last rect of the snake body and remove it
            tail = self.snake.pop()
            tail_rect = self.snake_rects.pop()
            self.board[tail[1]][tail[0]] = 0
            tail_rect.setFill('black')
        
        return False

    def generate_new_food(self):
        while True:
            random_x = random.randint(0, self.width-1)
            random_y = random.randint(0, self.height-1)
            if (random_x, random_y) not in self.snake:
                break
        self.board[random_y][random_x] = 2
        self._draw_rect(random_x, random_y, 'white')
        return (random_x, random_y)

    def _draw_rect(self, x, y, color):
        pos_x = x * self.cell_width
        pos_y = y * self.cell_height
        rect = Rectangle(Point(pos_x, pos_y), Point(pos_x + self.cell_width, pos_y + self.cell_height))
        rect.setFill(color)
        rect.draw(self.window)
        return rect
    
    def outside_board(self, x, y):
        return x < 0 or x > self.width-1 or y < 0 or y > self.height-1
    
    def get_visions(self):
        visions = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                x, y = tuple(map(operator.add, self.snake[0], (i, j)))
                vector = []
                while not self.outside_board(x, y):
                    vector.append(self.board[y][x])
                    x += i
                    y += j
                food_dist = 0 if 2 not in vector else vector.index(2) + 1
                body_dist = 0 if 1 not in vector else vector.index(1) + 1
                wall_dist = len(vector)
                visions += [food_dist, body_dist, wall_dist]
        return visions
    def to_string(self):
        string = ""
        for row in self.board:
            for cell in row:
                string += str(cell) + ' '
            string += '\n'
        return string
