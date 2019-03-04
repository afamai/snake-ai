class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[0 for x in range(width)] for y in range(height)]
    
    def set_cell(self, x, y, val):
        self.data[y][x] = val
    
    def clear_board(self):
        self.data = [[0 for x in range(self.width)] for y in range(self.height)]

    def clear_cell(self, x, y):
        self.data[y][x] = 0

    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height
    
    def __str__(self):
        string = ""
        for row in self.data:
            for cell in row:
                string += str(cell) + ' '
            string += '\n'
        return string

if __name__ == '__main__':
    board = Board(6, 6)