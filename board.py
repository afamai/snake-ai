class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[0] * width] * height
    
    def set_cell(self, x, y, val):
        self.data[x][y] = val
    
    def clear_cell(self, x, y):
        self.data[x][y] = 0

    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height
    
if __name__ == '__main__':
    board = Board(6, 6)