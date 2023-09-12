import grid
import random
import copy

from grid import Grid

class Sudoku():
    def __init__(self):
        self.Grid = Grid()
        self.complete = False
    #hàm lấy grid
    def get_Grid(self):
        return self.Grid
    
    #Hàm lấy về sudoku khác nhau giữa 2 sudoku
    def get_different(self, sudoku_temp):
        temp = Sudoku()

        for i in range(0,9):
            for j in range(0,9):
                if self.get_Grid().get_value_grid(i,j) != sudoku_temp.get_Grid().get_value_grid(i,j):
                    temp.get_Grid().add_value_grid(i,j,self.get_Grid().get_value_grid(i,j))
        return temp

    #Hàm kiểm tra xem giá trị nhập vào có hợp lệ không
    def is_valid_value(self, row, col, value):
        # Kiểm tra hàng và cột
        for i in range(9):
            if self.Grid.get_value_grid(row,i) == value or self.Grid.get_value_grid(i,col) == value:
                return False

        # Kiểm tra ở trong ô 3x3
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.Grid.get_value_grid(i,j) == value:
                    return False
        return True
    
    #Hàm tìm ô trống tiếp theo
    def _private_find_empty_cell(self , current_cell):
        for row in range(current_cell[0], 9):
            for col in range(current_cell[1], 9):
                if self.Grid.get_value_grid(row,col) == 0:
                    return (row, col)
        for row in range(0, 9):
            for col in range(0, 9):
                if self.Grid.get_value_grid(row,col) == 0:
                    return (row, col)
        return None
    #Hàm giải ma trận sudoku
    def solve_sudoku(self):
        current_cell = self._private_find_empty_cell( (0, 0) )
        if current_cell is None:
            self.complete = True
            return True

        row, col = current_cell

        for value in range(1, 10):
            if self.is_valid_value( row, col, value):
                self.Grid.add_value_grid(row, col, value)
                if self.solve_sudoku():
                    self.complete = True
                    return True

                self.Grid.add_value_grid(row, col, 0)

        return False

    #Hàm kiểm tra ma trận đã hoàn thành hay chưa
    def is_sudoku_completed(self):
            return self.complete
    
    #hàm khởi tạo ma trận ngẫu nhiên
    def ramdon_sudoku(self, level):
        self.Grid.add_level(level)
        temp = Sudoku()
        temp.Grid.add_level(level)
        if level == 'easy':
            level = 2
        elif level == 'balanced':
            level = 4
        elif level == 'hard':
            level = 5
        elif level == 'quite hardly':
            level = 9
        elif level == 'very hardly':
            level = 12
        k = 0
        randomnumber = list(range(1, 10))
        random.shuffle(randomnumber)

        
        for i in range(9):
            for j in range(9):
                self.Grid.add_value_grid(i,j, 0)
                if (j + 2) % 2 == 0 and (i + 2) % 2 == 0:
                    self.Grid.add_value_grid(i,j, randomnumber[k])
                    k += 1
                    if k == 9:
                        k = 0
        
        self.solve_sudoku()
        rann = random.randint(0, level - 1)
        c = 0
        
        for i in range(9):
            for j in range(9):
                temp.Grid.add_value_grid(i,j,0)
                if c < rann:
                    c += 1
                    continue
                else:
                    rann = random.randint(0, level - 1)
                    c = 0
                    temp.Grid.add_value_grid(i,j, self.Grid.get_value_grid(i,j))
        return temp
                
