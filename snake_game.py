from snake import *
from board import *
from graphics import *
from msvcrt import getch
import random
class SnakeGame:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    def __init__(self, window, snake, board):
        self.snake = snake
        self.board = board
        self.window = window
        
        # draw the board
        self.cell_width = window.getWidth() / self.board.get_width()
        self.cell_height = window.getHeight() / self.board.get_height()

        # draw the snake
        self.snake_rects = []
        for (x, y) in self.snake.get_body():
            self.board.set_cell(x, y, 0.5)
            rect = self._draw_rect(x, y)
            self.snake_rects.append(rect)
        
        self.food = self.generate_new_food()
        self.point = 0
    
    def update(self, key):
        # key = self.window.checkKey()
        if (key == 'Up' and self.snake.get_direction() != self.DOWN):
            self.snake.set_direction(self.UP)
        elif (key == 'Down' and self.snake.get_direction() != self.UP):
            self.snake.set_direction(self.DOWN)
        elif (key == 'Right' and self.snake.get_direction() != self.LEFT):
            self.snake.set_direction(self.RIGHT)
        elif (key == 'Left' and self.snake.get_direction() != self.RIGHT):
            self.snake.set_direction(self.LEFT)
        
        # move the snake
        tail = self.snake.move()
        new_pos = self.snake.get_body()[0]

        # check if the snake is in the zone or dead
        if (self.snake.is_dead() or new_pos[0] < 0 or new_pos[0] > self.board.get_width()-1 or new_pos[1] < 0 or new_pos[1] > self.board.get_height()-1):
            print('Game Over')
            self.window.close()
            return True

        # draw the new head
        self.board.set_cell(new_pos[0], new_pos[1], 0.5)
        head = self._draw_rect(new_pos[0], new_pos[1])
        self.snake_rects.insert(0, head)

        if new_pos == self.food:
            self.point += 1
            self.snake.get_body().append(tail)
            self.food = self.generate_new_food()
        else:
            # clear the last rect of the snake body and remove it
            tail_rect = self.snake_rects.pop()
            self.board.clear_cell(tail[0], tail[1])
            tail_rect.setFill('black')
        
        return False

    def generate_new_food(self):
        while True:
            random_x = random.randint(0, self.board.get_width()-1)
            random_y = random.randint(0, self.board.get_height()-1)
            if (random_x, random_y) not in self.snake.get_body():
                break
        self.board.set_cell(random_x, random_y, 1)
        self._draw_rect(random_x, random_y)
        return (random_x, random_y)

    def _draw_rect(self, x, y):
        pos_x = x * self.cell_width
        pos_y = y * self.cell_height
        rect = Rectangle(Point(pos_x, pos_y), Point(pos_x + self.cell_width, pos_y + self.cell_height))
        rect.setFill('white')
        rect.draw(self.window)
        return rect

