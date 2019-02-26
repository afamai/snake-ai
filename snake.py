import operator
class Snake:
    def __init__(self, x, y, direction, length):
        self.body = []
        self.direction = direction
        for i in range(length):
            self.body.append((x + i * -direction[0], y + i * -direction[1]))

    def set_direction(self, direction):
        self.direction = direction
    
    def get_direction(self):
        return self.direction

    def move(self):
        self.body.insert(0, tuple(map(operator.add, self.body[0], self.direction)))
        return self.body.pop()

    def get_body(self):
        return self.body
    
    def is_dead(self):
        return self.body[0] in self.body[1:]
    