from graphics import GraphWin, Rectangle, Point
from msvcrt import getch
import numpy as np
import operator
import random
class Game:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    def __init__(self, width, height, window):
        # create board
        self.width = width
        self.height = height

        self.board = [[0 for x in range(width)] for y in range(height)]
        self.window = window

        self.cell_width = window.getWidth() / width
        self.cell_height = window.getHeight() / height
    
    def start(self, snake):
        self.snake = snake       
        
        # draw the snake
        self.snake_rects = []
        for (x, y) in self.snake.body:
            self.board[y][x] = 1
            rect = self._draw_rect(x, y, 'white')
            self.snake_rects.append(rect)
        
        # generate food
        self.food = self.generate_new_food()

        self.over = False

    def reset(self):
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

        # clear the snake
        self.snake_rects = []
        for (x, y) in self.snake:
            self.board[y][x] = 1
            rect = self._draw_rect(x, y, 'black')
            self.snake_rects.append(rect)

        # clear the food
        self._draw_rect(self.food[0], self.food[1], 'black')

    def update(self):
        key = self.window.checkKey()

        if (key == 'Up' and self.snake.direction != self.DOWN):
            self.snake.direction = self.UP
        elif (key == 'Down' and self.snake.direction != self.UP):
            self.snake.direction = self.DOWN
        elif (key == 'Right' and self.snake.direction != self.LEFT):
            self.snake.direction = self.RIGHT
        elif (key == 'Left' and self.snake.direction != self.RIGHT):
            self.snake.direction = self.LEFT
        
        tail = self.snake.move()
        if self.snake.body[0] == self.food:
            self.snake.grow(tail)
            self.food = self.generate_new_food()
        else:
            tail_rect = self.snake_rects.pop()
            tail_rect.setFill('black')
            self.board[tail[1]][tail[0]] = 0

        if self.outside_board(self.snake.body[0]):
            self.snake.alive = False
        else:
            head = self.snake.body[0]
            head_rect = self._draw_rect(head[0], head[1], 'white')
            self.snake_rects.insert(0, head_rect)
            self.board[head[1]][head[0]] = 1
        
        if not self.snake.alive:
            self.over = True
            return

    def generate_new_food(self):
        while True:
            random_x = random.randint(0, self.width-1)
            random_y = random.randint(0, self.height-1)
            if (random_x, random_y) not in self.snake.body:
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
    
    def outside_board(self, pos):
        x = pos[0]
        y = pos[1]
        return x < 0 or x > self.width-1 or y < 0 or y > self.height-1

    def __str__(self):
        string = ""
        for row in self.board:
            for cell in row:
                string += str(cell) + ' '
            string += '\n'
        return string
