from genome import Genome
import operator
class Snake(Genome):
    def __init__(self, x, y, direction, length):
        self.start_x = x
        self.start_y = y
        self.body = []
        self.direction = direction
        self.alive = True
        self.left_to_live = 200
        self.vision = []
        Genome.__init__(self, 24, 4)

        for i in range(length):
            self.body.append((x + i * -direction[0], y + i * -direction[1]))

    def move(self):
        self.body.insert(0, tuple(map(operator.add, self.body[0], self.direction)))
        tail = self.body.pop()
        self.left_to_live -= 1
        self.fitness_score += 1
        if self.body[0] in self.body[1:] or self.left_to_live <= 0:
            self.alive = False
        return tail

    def grow(self, tail):
        self.body.append(tail)
        self.left_to_live += 100
        self.fitness_score += 100

    def look(self, board):
        vision = []
        height = len(board)
        width = len(board[0])
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                x, y = tuple(map(operator.add, self.body[0], (i, j)))
                vector = []
                while x >= 0 and x < width and y >= 0 and y < height:
                    vector.append(board[y][x])
                    x += i
                    y += j
                food_dist = 0 if 2 not in vector else vector.index(2) + 1
                body_dist = 0 if 1 not in vector else vector.index(1) + 1
                wall_dist = len(vector)
                vision += [1/food_dist, 1/body_dist, 1/wall_dist]