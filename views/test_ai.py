import pygame

from .view_management.view_template import GameView

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import GamePlay


from config.config import *


class TestAIView(GameView):

    def __init__(self, best_network):
        super().__init__()

        self.best_network = best_network

        self.name = 'test_ai'

        self.game = GamePlay()

        self.ai_bird = Bird(x=INITIAL_BIRD_X,
                            y=INITIAL_BIRD_Y, bird_type='ai')

    def _main_loop(self):

        super()._main_loop()

        self._make_ai_choose_jump()

        self._update_score(with_bird=self.ai_bird)

    def _make_ai_choose_jump(self):

        if self.game.active:

            # Determine which pipe we must focus on (first or second)
            pipe_index = 0
            if len(self.pipes) > 1 and self.ai_bird.x > self.pipes[0].x + self.pipes[0].WIDTH:
                pipe_index = 1

            # Send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output_network = self.best_network.activate((self.ai_bird.y, abs(
                self.ai_bird.y - self.pipes[pipe_index].y_top), abs(self.ai_bird.y - self.pipes[pipe_index].y_bottom)))

            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output_network[0] > 0.5:
                self.ai_bird.jump()

    def _manage_collisions(self):

        if self.ai_bird.collide_base(self.base):
            self.game.active = False

        for pipe in self.pipes:
            if self.ai_bird.collide_pipe(pipe):
                self.game.active = False

    def _move_objects(self):

        super()._move_objects()

        # Bird
        self.ai_bird.move()

    def _redraw_window(self):

        super()._redraw_window()

        # AI bird
        self.ai_bird.draw(window=self.window)
