import pygame
import sys
import os

import color_game
import save_
from path import Path

dir = Path()

class Menu():
    def __init__(self):
        self.screen_menu_size = (840,600)
        self.screen_menu = pygame.display.set_mode(self.screen_menu_size)
        self.running_menu = True
        self.continue_game = False
        self.new_game = False
        self.exit_game = False
        pygame.font.init()
        self.screen_menu_background  = pygame.image.load(dir.get_path() + "/images/Designer.png")
        self.font_Menu = pygame.font.Font(dir.get_path() +'/fonts/OpenSans-Regular.ttf',35)
        pygame.display.set_caption("Sudoku Game")

    def init_Menu(self):
        self.continue_game = False
        self.new_game = False
        self.exit_game = False

    def is_continue(self):
        return self.continue_game

    def is_new(self):
        return self.new_game
    
    def is_exit(self):
        return self.exit_game
    
    def status_running(self):
        return self.running_menu
    
    def start_running(self):
        self.running_menu = True
    
    #Kiểm tra có file save hay không 
    
    #vẽ chữ và đường viền cho button
    def draw_button(self, button_ ,button_size, location, text, color_boder, color_text):
            #vẽ đường viền
            border_thickness = 2
            pygame.draw.rect(self.screen_menu, color_boder , button_, border_thickness)
            #vẽ chữ
            result_text = self.font_Menu.render(text, True, color_text)
            #kích thướt của chữ
            text_rect = result_text.get_rect()
            self.screen_menu.blit(result_text, (location[0] + (button_size[0] - text_rect.width)/ 2, location[1]  +  (button_size[1] - text_rect.height) / 2 ))

    def loop(self):
        clock = pygame.time.Clock()
        self.screen_menu.blit(self.screen_menu_background, (0, 0))

        
        while self.running_menu:
            # Vẽ hình chữ nhật đại diện cho button
            Continue_button = pygame.Rect((320, 200), (200, 60))
            if save_.check_save():
                pygame.draw.rect(self.screen_menu, color_game.button_color_continue, Continue_button)
            else:
                pygame.draw.rect(self.screen_menu, color_game.color_button_disable, Continue_button)

            self.draw_button(Continue_button,[200,60], [320,200],'Chơi tiếp',color_game.WHITE,color_game.WHITE)
            # # Vẽ đường viền xung quanh button
            # border_thickness = 2
            # pygame.draw.rect(self.screen_menu, color_game.WHITE, Continue_button, border_thickness)
            # #Vẽ chữ vào button chơi tiếp
            # text_continue = self.font_Menu.render("Chơi tiếp", True, color_game.WHITE)
            # self.screen_menu.blit(text_continue, ( 350 , 205 ))

            # Vẽ hình chữ nhật đại diện cho button
            New_button = pygame.Rect((320, 280), (200, 60))
            pygame.draw.rect(self.screen_menu, color_game.button_color_new, New_button)
            # Vẽ đường viền xung quanh button
            border_thickness = 2
            pygame.draw.rect(self.screen_menu, color_game.WHITE, New_button, border_thickness)
            #Vẽ chữ vào button chơi mới
            text_new = self.font_Menu.render("Chơi Mới", True, color_game.WHITE)
            self.screen_menu.blit(text_new, ( 350 , 285 ))

            # Vẽ hình chữ nhật đại diện cho button
            Exit_button = pygame.Rect((320, 360), (200, 60))
            pygame.draw.rect(self.screen_menu, color_game.button_color_exit, Exit_button)
            # Vẽ đường viền xung quanh button
            border_thickness = 2
            pygame.draw.rect(self.screen_menu, color_game.WHITE, Exit_button, border_thickness)
            #Vẽ chữ vào button thoát
            text_exit = self.font_Menu.render("Thoát", True, color_game.WHITE)
            self.screen_menu.blit(text_exit, ( 375 , 365 ))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if Continue_button.collidepoint(event.pos) and save.check_save():
                        self.init_Menu()
                        self.continue_game = True
                        self.running_menu = False
                    if New_button.collidepoint(event.pos):
                        self.init_Menu()
                        self.new_game = True
                        self.running_menu = False
                    if Exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()
        # Kết thúc Pygame
        clock.tick(60)
