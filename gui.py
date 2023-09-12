import pygame
import sys
import copy
import time
import numpy as np

import color_game
import draw_button
import save_

from sudoku import Sudoku
from path import Path

duong_dan_goc = Path()

class Gui():
    def __init__(self, ):
        self.screen_Gui_size = (840,600)
        self.CELL_SIZE = 50
        self.GRID_SIZE = self.CELL_SIZE * 9
        self.screen_Gui = pygame.display.set_mode(self.screen_Gui_size)
        self.running_Gui = False
        self.selected_cell = None
        self.level = None
        self.check_all_answer = False
        self.check_answer = False
        self.solve_answer = False
        self.exit_game = False
        self.save_grid = 0
        self.save_game = False
        self.back_menu = False
        self.fail = 0
        pygame.font.init()
        self.screen_Gui_background  = pygame.image.load(duong_dan_goc.get_path() +"/images/Designer.png")
        self.font_Gui = pygame.font.Font(duong_dan_goc.get_path() + '/fonts/OpenSans-Regular.ttf',35)
        pygame.display.set_caption("Sudoku Game")

    def init_Gui(self):
        self.check_all_answer = False
        self.check_answer = False
        self.solve_answer = False
        self.exit_game = False
        self.save_grid = 0
        self.save_game = False
        self.back_menu = False

    #hàm trả về gui loop có đang chạy hay k
    def status_running(self):
        return self.running_Gui

    #hàm khởi chạy giao diện
    def start_running(self):
        self.running_Gui = True

    #hàm trả về trạng thái trở về menu
    def status_back_menu(self):
        self.back_menu
    
    # Hàm kiểm tra ô đã được chọn
    def get_selected_cell(self, mouse_pos):
        row = (mouse_pos[0] - 195) // self.CELL_SIZE
        col = (mouse_pos[1] - 75) // self.CELL_SIZE
        if row >= 0 and row < 9 and col >=0 and col <9 :
            return (row, col)
        return None
    # Hàm vẽ lưới Sudoku
    def draw_grid(self, distance_row, distance_col):

        for i in range(10):
            if i % 3 != 0:
                line_color = color_game.BLACK
                pygame.draw.line(self.screen_Gui, line_color, (distance_row, distance_col + i * self.CELL_SIZE), (distance_row + self.GRID_SIZE, distance_col + i * self.CELL_SIZE),1)
                pygame.draw.line(self.screen_Gui, line_color, (distance_row + i * self.CELL_SIZE, distance_col), (distance_row + i * self.CELL_SIZE, distance_col + self.GRID_SIZE),1)
        for i in range(10):
            if i % 3 == 0:
                line_color = color_game.BLACK
                pygame.draw.line(self.screen_Gui, line_color, (distance_row, distance_col + i * self.CELL_SIZE), (distance_row + self.GRID_SIZE, distance_col + i * self.CELL_SIZE),4)
                pygame.draw.line(self.screen_Gui, line_color, (distance_row + i * self.CELL_SIZE, distance_col), (distance_row + i * self.CELL_SIZE,distance_col + self.GRID_SIZE),4)
    # Hàm vẽ số vào ô Sudoku
    def draw_number(self, row, col, number, distance_row, distance_col):
        font_number = pygame.font.SysFont('OpenSans-Regular.ttf', 48)
        text = font_number.render(str(number), True, color_game.BLACK)

        x = distance_row +  col * self.CELL_SIZE + self.CELL_SIZE // 2 - text.get_width() // 2
        y = distance_col + row * self.CELL_SIZE + self.CELL_SIZE // 2 - text.get_height() // 2

        # pygame.draw.rect(window, WHITE, (10 + col * CELL_SIZE, 5 + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),1)
        self.screen_Gui.blit(text, (x, y))

    #vẽ màu lên ô vuông
    def draw_color_square(self,color_square ,distance_row,distance_col, j , i):
         pygame.draw.line(self.screen_Gui, color_square, ( distance_row + j * self.CELL_SIZE + 25, distance_col + i * self.CELL_SIZE), (distance_row + j * self.CELL_SIZE + 25,50 + distance_col + i * self.CELL_SIZE), 50)

    # Hàm vẽ màu bảng Sudoku
    def draw_board(self,sudoku_temp ,distance_row, distance_col ):
        for i in range(9):
            for j in range(9):
                if sudoku_temp.get_Grid().get_value_grid(i,j) != 0 :
                    # pygame.draw.rect(window, BLUE, (1 + i % 3 + 50 * i, j % 3 +51 * j, 47, 47))
                    self.draw_color_square(color_game.BLUE, distance_row, distance_col ,j,i)
                else: 
                    self.draw_color_square(color_game.WHITE, distance_row, distance_col ,j,i)
                # if sudoku_different.get_Grid().get_value_grid(i,j) != 0:
                #     self.draw_color_square(color_game.RED, distance_row, distance_col ,j,i)

    # Hàm vẽ màu bảng Sudoku khi kiểm tra sai
    def draw_board_different(self,sudoku_different ,distance_row, distance_col ):
        for i in range(9):
            for j in range(9):
                 if sudoku_different.get_Grid().get_value_grid(i,j) != 0:
                    self.draw_color_square(color_game.RED, distance_row, distance_col ,j,i)

    #đường viền và chữ lên button
    def draw_button(self, button_ ,button_size, location, text, font_size, color_boder, color_text):
            #vẽ đường viền
            border_thickness = 2
            pygame.draw.rect(self.screen_Gui, color_boder , button_, border_thickness)
            #vẽ chữ
            result_text = self.font_Gui.render(text, True, color_text)
            #kích thướt của chữ
            text_rect = result_text.get_rect()
            self.screen_Gui.blit(result_text, (location[0] + (button_size[0] - text_rect.width)/ 2, location[1]  +  (button_size[1] - text_rect.height) / 2 ))

    #
    def loop(self, continue_game):
        result = None
        result_color= None
        clock = pygame.time.Clock()
        sudoku = Sudoku()      #Bảng lưu ma trận khi đang chơi
        sudoku_temp = Sudoku()    #Bảng lưu ma trận gốc
        sudoku_solved = Sudoku()
        sudoku_different = Sudoku()
        start_time = None

        if continue_game:
            sudoku , sudoku_temp = save_.read_file_save()
            # sudoku_temp = copy.deepcopy(sudoku)
            sudoku_solved = copy.deepcopy(sudoku_temp)
            sudoku_solved.solve_sudoku()
            self.level = 'playing'
            self.fail = 5
        while self.running_Gui:
                
            self.screen_Gui.blit(self.screen_Gui_background, (0, 0))
            #vẽ button chế độ chơi dễ
            button_easy = pygame.Rect( 10, 75 , 175, 50)
            pygame.draw.rect(self.screen_Gui,color_game.color_button, button_easy)
            #Vẽ chữ lên button dễ 
            draw_button.Draw_button( button_easy, self.screen_Gui, [175,50], [10, 75], 'Dễ', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button chế độ chơi trung bình
            button_balanced = pygame.Rect( 10, 135 , 175, 50)
            pygame.draw.rect(self.screen_Gui,color_game.color_button, button_balanced)
            #Vẽ chữ lên button khó
            draw_button.Draw_button( button_balanced,self.screen_Gui, [175,50], [10, 135], 'Trung bình', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button chế độ chơi Khó
            button_hard = pygame.Rect( 10, 195 , 175, 50)
            pygame.draw.rect(self.screen_Gui,color_game.color_button, button_hard)
            #Vẽ chữ lên button Khó
            draw_button.Draw_button( button_hard,self.screen_Gui, [175,50], [10, 195], 'Khó', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button chế độ khá Khó
            button_score_fail = pygame.Rect( 10, 255 , 175, 50)
            pygame.draw.rect(self.screen_Gui,color_game.color_button, button_score_fail)
            #Vẽ chữ lên button khá Khó
            draw_button.Draw_button( button_score_fail,self.screen_Gui, [175,50], [10, 255],'Số lần sai: ' + str(5 - self.fail), 60 , color_game.WHITE , color_game.WHITE )

            # #vẽ button chế độ chơi rất Khó
            # button_very_hardly = pygame.Rect( 10, 315 , 175, 50)
            # pygame.draw.rect(self.screen_Gui,color_game.color_button, button_very_hardly)
            # #Vẽ chữ lên button rất Khó
            # draw_button.Draw_button( button_very_hardly,self.screen_Gui, [175,50], [10, 315], 'Rất Khó', 60 , color_game.WHITE , color_game.WHITE )


            #vẽ button Kiểm tra đáp án
            button_check_all = pygame.Rect( 665, 75 , 175, 50)
            if not sudoku.is_sudoku_completed() and self.level is not None and self.fail >= 0:
                pygame.draw.rect(self.screen_Gui,color_game.color_button, button_check_all)
            else :
                pygame.draw.rect(self.screen_Gui,color_game.color_button_disable, button_check_all)
            #Vẽ chữ lên button Kiểm tra đáp án 
            draw_button.Draw_button( button_check_all,self.screen_Gui, [175,50], [665, 75], 'Kiểm tra', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button kiểm tra một ô
            button_check = pygame.Rect( 665, 135 , 175, 50)
            if not sudoku.is_sudoku_completed() and self.level is not None and self.selected_cell and self.fail >= 0:
                row, col = self.selected_cell
                # print(row)
                # print(col)
                if sudoku.get_Grid().get_value_grid(col,row) != 0:
                    pygame.draw.rect(self.screen_Gui,color_game.color_button, button_check)
                else:
                    pygame.draw.rect(self.screen_Gui,color_game.color_button_disable, button_check)
            else:
                pygame.draw.rect(self.screen_Gui,color_game.color_button_disable, button_check)
            #Vẽ chữ lên button giải ma trận
            draw_button.Draw_button( button_check,self.screen_Gui, [175,50], [665, 135], 'kiểm tra ô', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button giải ma trận
            button_solve = pygame.Rect( 665, 195 , 175, 50)
            if not sudoku.is_sudoku_completed() and self.level is not None:
                pygame.draw.rect(self.screen_Gui,color_game.color_button, button_solve)
            else:
                pygame.draw.rect(self.screen_Gui,color_game.color_button_disable, button_solve)
            #Vẽ chữ lên button giải ma trận
            draw_button.Draw_button( button_solve,self.screen_Gui, [175,50], [665, 195], 'Giải ma trận', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button lưu ma trận
            button_save_grid = pygame.Rect( 665, 255 , 175, 50)
            if sudoku.is_sudoku_completed() and self.level is not None and self.save_grid == 0:
                pygame.draw.rect(self.screen_Gui,color_game.color_button, button_save_grid)
            else: 
                pygame.draw.rect(self.screen_Gui,color_game.color_button_disable, button_save_grid)
            #Vẽ chữ lên button lưu ma trận
            draw_button.Draw_button( button_save_grid,self.screen_Gui, [175,50], [665, 255], 'lưu ma trận', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button lưu game
            button_save_game = pygame.Rect( 665, 315 , 175, 50)
            if  self.level is not None and not sudoku.is_sudoku_completed():
                pygame.draw.rect(self.screen_Gui,color_game.color_button, button_save_game)
            else:
                pygame.draw.rect(self.screen_Gui,color_game.color_button_disable, button_save_game)
            #Vẽ chữ lên button lưu game
            draw_button.Draw_button( button_save_game,self.screen_Gui, [175,50], [665, 315], 'Lưu game', 60 , color_game.WHITE , color_game.WHITE )

            #vẽ button về menu
            button_back_menu = pygame.Rect( 665, 375 , 175, 50)
            pygame.draw.rect(self.screen_Gui,color_game.color_button, button_back_menu)
            #Vẽ chữ lên button về menu
            draw_button.Draw_button( button_back_menu,self.screen_Gui, [175,50], [665, 375], 'Menu', 60 , color_game.WHITE , color_game.WHITE )

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_easy.collidepoint(event.pos):
                        self.init_Gui()
                        self.level = 'easy'
                    elif button_balanced.collidepoint(event.pos):
                        self.init_Gui()
                        self.level = 'balanced'
                    elif button_hard.collidepoint(event.pos):
                        self.init_Gui()
                        self.level = 'hard'
                    # elif button_quite_hardly.collidepoint(event.pos):
                    #     self.init_Gui()
                    #     self.level = 'quite hardly'
                    # elif button_very_hardly.collidepoint(event.pos):
                    #     self.init_Gui()
                    #     self.level = 'very hardly'
                    elif button_check_all.collidepoint(event.pos):
                        self.check_all_answer = True
                    elif button_check.collidepoint(event.pos):
                        self.check_answer = True
                    elif button_solve.collidepoint(event.pos):
                        self.init_Gui()
                        self.solve_answer = True
                    elif button_save_grid.collidepoint(event.pos):
                        if self.save_grid == 0:
                            self.save_grid = 1
                    elif button_save_game.collidepoint(event.pos):
                        self.save_game = True
                    elif button_back_menu.collidepoint(event.pos):
                        self.init_Gui()
                        self.back_menu = True
                        self.running_Gui = False
                    elif event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        self.selected_cell = self.get_selected_cell(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    if self.selected_cell is not None and self.fail >= 0:
                        col, row = self.selected_cell
                        if event.key == pygame.K_1:
                                sudoku.get_Grid().add_value_grid(row, col , 1)
                        elif event.key == pygame.K_2:
                                sudoku.get_Grid().add_value_grid(row, col , 2)
                        elif event.key == pygame.K_3:
                                sudoku.get_Grid().add_value_grid(row, col , 3)
                        elif event.key == pygame.K_4:
                               sudoku.get_Grid().add_value_grid(row, col , 4)                            
                        elif event.key == pygame.K_5:
                                sudoku.get_Grid().add_value_grid(row, col , 5)                           
                        elif event.key == pygame.K_6:
                                sudoku.get_Grid().add_value_grid(row, col , 6)                            
                        elif event.key == pygame.K_7:
                                sudoku.get_Grid().add_value_grid(row, col , 7)                            
                        elif event.key == pygame.K_8:
                                sudoku.get_Grid().add_value_grid(row, col , 8)                            
                        elif event.key == pygame.K_9:
                                sudoku.get_Grid().add_value_grid(row, col , 9)                            
                        elif event.key == pygame.K_BACKSPACE:
                            sudoku.get_Grid().add_value_grid(row, col , 0)
                    
            if self.level == 'easy':
                sudoku_different = Sudoku()
                sudoku = sudoku_solved.ramdon_sudoku(self.level)
                sudoku_temp = copy.deepcopy(sudoku)
                self.fail = 5
                self.level = 'playing'
            if self.level == 'balanced':
                sudoku_different = Sudoku()
                sudoku = sudoku_solved.ramdon_sudoku(self.level)
                sudoku_temp = copy.deepcopy(sudoku)
                self.fail = 5
                self.level = 'playing'
            if self.level == 'hard':
                sudoku_different = Sudoku()
                sudoku = sudoku_solved.ramdon_sudoku(self.level)
                sudoku_temp = copy.deepcopy(sudoku)
                self.fail = 5
                self.level = 'playing'
            # if self.level == 'quite hardly':
            #     sudoku_different = Sudoku()
            #     sudoku = sudoku_solved.ramdon_sudoku(self.level)
            #     sudoku_temp = copy.deepcopy(sudoku)
            #     self.level = 'playing'
            # if self.level == 'very hardly':
            #     sudoku_different = Sudoku()
            #     sudoku = sudoku_solved.ramdon_sudoku(self.level)
            #     sudoku_temp = copy.deepcopy(sudoku)
            #     self.level = 'playing'
            if self.check_all_answer and self.level is not None and not sudoku.is_sudoku_completed() and self.fail >= 0:
                if sudoku.get_Grid().get_grid() ==  sudoku_solved.get_Grid().get_grid():
                    result = "Bạn đã giải ma trận thành công"
                    complete_grid = True
                    result_color = color_game.CHOCOLATE
                    start_time = time.time()
                else:
                    sudoku_different = sudoku.get_different(sudoku_solved)
                    result = "Đáp án của bạn chưa chính xác"
                    result_color = color_game.DARK_RED
                    self.fail = self.fail - 1
                    start_time = time.time()
                
                self.check_all_answer    = False

            if self.check_answer and self.selected_cell is not None and self.fail >= 0:
                row, col = self.selected_cell
                
                if sudoku.get_Grid().get_value_grid(col,row) != 0:
                    if sudoku.get_Grid().get_value_grid(col,row) == sudoku_solved.get_Grid().get_value_grid(col,row):
                        result = 'Vị trí bạn đã điền số đúng'
                        result_color = color_game.CHOCOLATE
                        start_time = time.time()
                    else:
                        result = 'Vị trí bạn đã điền số sai'
                        self.fail = self.fail - 1
                        result_color = color_game.DARK_RED
                        start_time = time.time()
                self.check_answer = False
            
            if self.solve_answer and not sudoku.is_sudoku_completed():
                result = "Ma trận đã được giải"
                result_color = color_game.CHOCOLATE
                sudoku = copy.deepcopy(sudoku_solved)
                start_time = time.time()

            if self.save_game and self.level is not None and not sudoku.is_sudoku_completed():
                save_.Save_Grid(sudoku.get_Grid(),sudoku_temp.get_Grid())
                result = 'Bạn đã lưu game thành công'
                result_color = color_game.CHOCOLATE
                self.save_game = False
                start_time = time.time()

            if self.save_grid == 1 and sudoku.is_sudoku_completed():
                save_.Save_game(sudoku_temp.get_Grid(),sudoku_solved.get_Grid())
                result = 'Bạn đã lưu ma trận thành công'
                result_color = color_game.CHOCOLATE
                self.save_grid = 2
                start_time = time.time()

            if start_time is not None:
                
                # Kiểm tra thời gian hiển thị chữ
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                if elapsed_time > 3:
                    result = None
                    start_time = None
                    current_time = None

            if result is not None and result_color is not None and self.fail >= 0:
                result_text = self.font_Gui.render(result, True, result_color )
                self.screen_Gui.blit(result_text, (195, 28))
            
            if self.fail < 0:
                result_fail = self.font_Gui.render('Bạn đã sai quá 5 lần!', True, color_game.RED )
                self.screen_Gui.blit(result_fail, (195, 28))
            
            self.draw_board(sudoku_temp,195, 75)
            
            self.draw_board_different(sudoku_different,195,75)
            self.draw_grid(195, 75)
            # self.draw_diferent(sudoku_different,195, 75)
            if self.selected_cell is not None:
                row, col = self.selected_cell
                if row >= 0 and row < 9 and col >=0 and col <9 :
                    if sudoku_temp.get_Grid().get_value_grid(col, row) == 0:
                        pygame.draw.rect(self.screen_Gui, (238 ,238, 0), (195 + row * self.CELL_SIZE,75 + col * self.CELL_SIZE,  self.CELL_SIZE , self.CELL_SIZE), 4)
                    else:
                            self.selected_cell = None
            for row in range(9):
                for col in range(9):
                    number = sudoku.get_Grid().get_value_grid(row,col)
                    if number != 0:
                        # given = True if self.selected_cell == (row, col) else False
                        self.draw_number(row, col, number,195, 75 )
        
            pygame.display.flip()
        #fps cho game
        clock.tick(60)
# a = Gui()
# a.start_running()
# a.loop()