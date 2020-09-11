import pygame

from .view_management.view_template import View
from objects.visual_objects import Bird, Pipe, Base

from config import *


class MainView(View):

    def __init__(self):
        super().__init__()

        self.name = 'main'

        self.bird = Bird(x=INITIAL_BIRD_X,
                         y=INITIAL_BIRD_Y)
        self.pipe = Pipe(x=INITIAL_PIPE_X)

        self.base = Base(y=INITIAL_BASE_Y)

    def _main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_window()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()

        self.pipe.move()
        self.bird.move()
        self.base.move()

        self._redraw_window()

    def _redraw_window(self):
        self.clock.tick(FPS)
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))
        self.bird.draw(window=self.window)

        # Draw the pipe first and then the base
        self.pipe.draw(window=self.window)
        self.base.draw(window=self.window)

        pygame.display.update()
