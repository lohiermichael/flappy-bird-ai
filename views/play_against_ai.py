import pygame

from .view_management.view_template import View

from objects.visual_objects import Bird, Pipe, Base
from objects.game_objects import GamePlayAgainAI
from objects.buttons import RectangularButton


from config.config import *


class PlayAgaintAI(View):

    def __init__(self, best_network):
        super().__init__()

        self.name = 'play_against_ai'

        self.game = GamePlayAgainAI()
        self.replay = False

        self.best_network = best_network

        self.ai_bird = Bird(x=INITIAL_BIRD_X,
                            y=INITIAL_BIRD_Y, bird_type='ai')

        self.player_bird = Bird(x=INITIAL_BIRD_X,
                                y=INITIAL_BIRD_Y, bird_type='player')

        self.birds = [self.ai_bird, self.player_bird]

        self.pipes = [Pipe(x=INITIAL_PIPE_X)]

        self.base = Base(y=INITIAL_BASE_Y)

        self.replay_button = RectangularButton(font=REPLAY_BUTTON_FONT,
                                               color=REPLAY_BUTTON_COLOR,
                                               border=True,
                                               center=REPLAY_BUTTON_CENTER,
                                               height=REPLAY_BUTTON_HEIGHT,
                                               width=REPLAY_BUTTON_WIDTH,
                                               text=REPLAY_BUTTON_TEXT)

    def _main_loop(self):

        self._manage_events()

        self._make_ai_choose_jump()

        self._manage_collisions()

        self._manage_pipes()

        self._move_objects()

        self._update_score()

        self._redraw_window()

        self._check_terminal_condition()

    def _manage_events(self):

        for event in pygame.event.get():
            # Quite the window
            if event.type == pygame.QUIT:
                self._quit_window()

            # Make the  player bird jump
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.active:
                self.player_bird.jump()

            # Restart the game
            elif event.type == pygame.MOUSEBUTTONUP and not self.game.active:
                if self.replay_button.is_under(pygame.mouse.get_pos()):
                    self.replay = True
                    self._quit_window()

    def _make_ai_choose_jump(self):

        # if self.game.active:

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

        # Birds
        self.ai_bird.move()
        self.player_bird.move()

    def _update_score(self):
        for pipe in self.pipes:
            # If the pipe is passed create a new one
            if not pipe.passed and pipe.x < self.player_bird.x:
                pipe.passed = True
                self.pipes.append(Pipe(x=INITIAL_PIPE_X))
                self.game.score += 1

    def _redraw_window(self):
        self.clock.tick(FPS)
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))

        for bird in self.birds:
            bird.draw(window=self.window)

        # Draw the pipe first and then the base
        for pipe in self.pipes:
            pipe.draw(window=self.window)

        self.base.draw(window=self.window)

        self.game.draw_score(window=self.window)

    def _check_terminal_condition(self):
        if len(self.birds) == 1:
            self.game.active = False

            self.game.draw_end_game(window=self.window,
                                    replay_button=self.replay_button)

        pygame.display.update()
