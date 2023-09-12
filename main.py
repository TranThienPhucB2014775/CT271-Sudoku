import pygame
import sys

from grid import Grid
from sudoku import Sudoku
from menu import Menu
from gui import Gui

def main():
    menu = Menu()
    gui = Gui()
    while True:
        menu.loop()
        if Menu.is_new:
            gui.start_running()
            # menu.init_Menu()
            gui.loop(menu.is_continue())
        if not gui.status_back_menu():
            menu.start_running()
            gui.init_Gui()
            menu.loop()


if __name__ == "__main__":
    main()