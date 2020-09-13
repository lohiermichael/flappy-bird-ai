import pygame

from .view_management.view_template import View

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import GamePlay

from config.config import *


class PlayView(View):

    def __init__(self):
        super().__init__()

        self.name = 'main'

        self.game = GamePlay()

        self.bird = Bird(x=INITIAL_BIRD_X,
                         y=INITIAL_BIRD_Y, bird_type='player')

        self.pipes = [Pipe(x=INITIAL_PIPE_X)]

    def _main_loop(self):

        super()._main_loop()

        self._manage_collisions()

        self._manage_pipes()

        self._move_objects()

        self._update_score()

    def _manage_event(self, event):

        super()._manage_event(event)

        # Make the bird jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.active:
            self.bird.jump()

    def _manage_click_events(self):
        super()._manage_click_events()
        super()._click_on_restart()

    def _manage_collisions(self):

        if self.bird.collide_base(self.base):
            self.game.active = False

        for pipe in self.pipes:
            if self.bird.collide_pipe(pipe):
                self.game.active = False

    def _manage_pipes(self):

        # Pipes to remove
        pipes_to_remove = []

        for pipe in self.pipes:
            # If it gets off the screen add it to the list to remove
            if pipe.x + pipe.WIDTH < 0:
                pipes_to_remove.append(pipe)

        for pipe_to_remove in pipes_to_remove:
            self.pipes.remove(pipe_to_remove)

    def _move_objects(self):

        if self.game.active:
            # Base
            self.base.move()
            # Pipes
            for pipe in self.pipes:
                pipe.move()

        # Bird
        self.bird.move()

    def _update_score(self):
        for pipe in self.pipes:
            # If the pipe is passed create a new one
            if not pipe.passed and pipe.x < self.bird.x:
                pipe.passed = True
                self.pipes.append(Pipe(x=INITIAL_PIPE_X))
                self.game.score += 1

    def _redraw_window(self):

        super()._redraw_window()

        # Bird
        self.bird.draw(window=self.window)

        # Pipes
        for pipe in self.pipes:
            pipe.draw(window=self.window)

        # Score
        self.game.draw_score(window=self.window)

        # End game
        if not self.game.active:
            self.game.draw_end_game(window=self.window,
                                    replay_button=self.replay_button)

        # Return button
        self.return_button.draw(window=self.window)
