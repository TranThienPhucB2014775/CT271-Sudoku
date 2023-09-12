class Grid():
    def __init__(self):
        self.grid = [[0] * 9 for _ in range(9)]
        self.level = None
    def new_game(self):
    # Khởi tạo ma trận Sudoku rỗng```python
        self.grid = [[0] * 9 for _ in range(9)]

        # Xóa tất cả các ô đã điền
        for row in range(9):
            for col in range(9):
                self.grid[row][col] = 0

        return self.grid
    
    #Hàm Thêm trá trị vào grid
    def add_value_grid(self, row, col, value):
        self.grid[row][col] = value

    #Hàm kiểm tra grid đã hoàn thành hay chưa
    def check_grid(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return False
        return True
    
    #Hàm lấy grid
    def get_grid(self):
        return self.grid
    
    
    #Hàm lấy giá trị tại vị trí row, col
    def get_value_grid(self, row, col):
        return self.grid[row][col]
    
    #hàm lấy level của ma trận
    def get_level(self):
        return self.level
    
    #hàm gán giá trị cấp độ ma trận
    def add_level(self,level_):
        self.level = level_

# a = Grid()
# a.get_value_grid(8,8)
    