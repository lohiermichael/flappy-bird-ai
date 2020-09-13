import pygame

from .view_management.view_template import GameView

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import GamePlayAgainAI


from config.config import *


class PlayAgaintAI(GameView):

    def __init__(self, best_network):
        super().__init__()

        self.name = 'play_against_ai'

        self.game = GamePlayAgainAI()

        self.best_network = best_network

        self.ai_bird = Bird(x=INITIAL_BIRD_X,
                            y=INITIAL_BIRD_Y, bird_type='ai')

        self.player_bird = Bird(x=INITIAL_BIRD_X,
                                y=INITIAL_BIRD_Y, bird_type='player')

        self.birds = [self.ai_bird, self.player_bird]

    def _main_loop(self):

        super()._main_loop()

        self._make_ai_choose_jump()

        self._update_score(with_bird=self.player_bird)

        self._check_terminal_condition()

    def _manage_event(self, event):
        super()._manage_event(event)

        # Make the bird jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.active:
            self.player_bird.jump()

    def _make_ai_choose_jump(self):

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

        if self.game.active:

            for bird in self.birds:

                if bird.collide_base(self.base):
                    self.birds.remove(bird)

                for pipe in self.pipes:
                    if bird.collide_pipe(pipe):
                        self.birds.remove(bird)
            # Determine the winner
            self.game.winner = self.birds[0]

    def _move_objects(self):

        if self.game.active:
            # Base
            self.base.move()
            # Pipes
            for pipe in self.pipes:
                pipe.move()

        # Birds
        self.ai_bird.move()
        self.player_bird.move()

    def _check_terminal_condition(self):
        if len(self.birds) == 1:
            self.game.active = False

            self.game.draw_end_game(window=self.window,
                                    replay_button=self.replay_button)

    def _redraw_window(self):
        super()._redraw_window()

        # Birds
        for bird in self.birds:
            bird.draw(window=self.window)
