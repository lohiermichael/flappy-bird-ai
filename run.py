import pygame

from views.main import MainView
from views.view_management.view_template import View

if __name__ == "__main__":
    pygame.init()
    replay = True
    while replay:
        main_view = MainView()
        main_view.start_main_loop()
        replay = main_view.replay
