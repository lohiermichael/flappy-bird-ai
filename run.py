import pygame

from views.main import MainView
from views.view_management.view_template import View

if __name__ == "__main__":
    pygame.init()
    main = MainView().start_main_loop()
    # view = View().start_main_loop()
