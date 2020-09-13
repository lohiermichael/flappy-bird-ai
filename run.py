import pygame

from views.view_management.view_flow import ViewFlow

if __name__ == "__main__":
    pygame.init()
    view_flow = ViewFlow()
    view_flow.run()
