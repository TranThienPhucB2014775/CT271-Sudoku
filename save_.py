import os
from datetime import datetime

from grid import Grid
from sudoku import Sudoku
from path import Path
def Save_game(grid, grid_temp):
        level = grid.get_level()
        grid = grid.get_grid()
        grid_temp = grid_temp.get_grid()
        # Lấy đường dẫn thư mục chứa file Python đang chạy
        duong_dan_goc = Path()

            # Tạo thư mục "log" nếu chưa tồn tại
        log = os.path.join(duong_dan_goc.get_path(), "log")
        os.makedirs(log, exist_ok=True)

            # Lấy thời gian hiện tại
        time_now = datetime.now()
        time_now = time_now.strftime("%d-%m-%Y %H-%M-%S")
            # Định dạng tên file
        ten_file ="Ma Trận ("+ time_now + ").txt"
            # Đường dẫn file
        duong_dan_file = os.path.join(log, ten_file)

            # Ma trận ban đầu và đáp án
        grid_ban_dau = '\n'.join('  '.join(str(x) for x in hang) for hang in grid)
        grid_dap_an  = '\n'.join('  '.join(str(x) for x in hang) for hang in grid_temp)


        with open(duong_dan_file, "w") as file:
            file.write(str(time_now))
            file.write("\n" +str(level))
            file.write("\n" + grid_ban_dau)
            file.write("\n        *********")
            file.write("\n" + grid_dap_an)

def check_save():
        duong_dan_goc = Path()
        duong_dan_goc = duong_dan_goc.get_path() + '\save'
        duong_dan_tap_tin = os.path.join(duong_dan_goc, "save.txt") 
        if not os.path.exists(duong_dan_tap_tin):
            return False
        with open(duong_dan_tap_tin, 'r') as file:
            dong_du_lieu = file.readlines()

            if len(dong_du_lieu) != 18:
                
                return False

            for dong in dong_du_lieu:
                gia_tri_dong = dong.strip().split()

                if len(gia_tri_dong) != 9:
                    return False

                try:
                    ma_tran_dong = [int(gia_tri) for gia_tri in gia_tri_dong]
                except ValueError:
                    return False

        return True
def read_file_save():
    duong_dan_goc = Path()
    duong_dan_goc = duong_dan_goc.get_path() + '\save'
    duong_dan_tap_tin = os.path.join(duong_dan_goc, "save.txt") 
    with open(duong_dan_tap_tin, 'r') as file:
        dong_du_lieu = file.readlines()

        ma_tran_1 = []
        ma_tran_2 = []
        k = 1
        for dong in dong_du_lieu:
            gia_tri_dong = [int(x) for x in dong.strip().split()]
            # if gia_tri_dong:
            #     k = k + 1
            #     print(k)
            if k <=9:
                ma_tran_1.append(gia_tri_dong)
                k = k + 1
            else:
                ma_tran_2.append(gia_tri_dong)

    sudoku_temp_1 = Sudoku()
    sudoku_temp_2 = Sudoku()
    for i in range(0,9):
         for j in range(0,9):
              sudoku_temp_1.get_Grid().add_value_grid(i, j, ma_tran_1[i][j])
    
    for i in range(0,9):
         for j in range(0,9):
              sudoku_temp_2.get_Grid().add_value_grid(i, j, ma_tran_2[i][j])
    # print(ma_tran_1)
    return (sudoku_temp_1, sudoku_temp_2)



def Save_Grid(grid,grid_playing):
        # level = grid.get_level()
        grid = grid.get_grid()
        grid_playing = grid_playing.get_grid()

        # Lấy đường dẫn thư mục chứa file Python đang chạy
        duong_dan_goc = Path()

            # Tạo thư mục "save" nếu chưa tồn tại
        log = os.path.join(duong_dan_goc.get_path(), "save")
        os.makedirs(log, exist_ok=True)

            # Đường dẫn file
        duong_dan_file = os.path.join(log,'save.txt')

            # Ma trận ban đầu và đáp án
        grid_ban_dau = '\n'.join('  '.join(str(x) for x in hang) for hang in grid)
        grid_dang_choi = '\n'.join('  '.join(str(x) for x in hang) for hang in grid_playing)

        with open(duong_dan_file, "w") as file:
            file.write(grid_ban_dau)
            file.write('\n'+grid_dang_choi)
# a = Sudoku()
# b = Sudoku()          
# a , b = read_file_save()
# print(b.get_Grid().get_value_grid(8,8))