import pygame

from .view_management.view_template import View
from objects.visual_objects import Bird

from config import *


class MainView(View):

    def __init__(self):
        super().__init__()

        self.name = 'main'

        self.bird = Bird(INITIAL_BIRD_X, INITIAL_BIRD_Y)

    def _main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_window()
            elif event.type == pygame.KEYDOWN:
                self.bird.jump()

        self.bird.move()

        self._redraw_window()

    def _redraw_window(self):
        self.clock.tick(FPS)
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))
        self.bird.draw(window=self.window)
        pygame.display.update()
