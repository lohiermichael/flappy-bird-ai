import pygame

from .view_management.view_template import GameView

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import GamePlay

from config.config import *


class PlayView(GameView):

    def __init__(self):
        super().__init__()

        self.name = 'main'

        self.game = GamePlay()

        self.bird = Bird(x=INITIAL_BIRD_X,
                         y=INITIAL_BIRD_Y, bird_type='player')

    def _main_loop(self):

        super()._main_loop()

        self._update_score(with_bird=self.bird)

    def _manage_event(self, event):

        super()._manage_event(event)

        # Make the bird jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.active:
            self.bird.jump()

    def _manage_collisions(self):

        if self.bird.collide_base(self.base):
            self.game.active = False

        for pipe in self.pipes:
            if self.bird.collide_pipe(pipe):
                self.game.active = False

    def _move_objects(self):

        super()._move_objects()

        # Bird
        self.bird.move()

    def _redraw_window(self):

        super()._redraw_window()

        # Bird
        self.bird.draw(window=self.window)
