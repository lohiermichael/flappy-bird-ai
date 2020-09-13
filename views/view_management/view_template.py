from objects.buttons import ImageButton, TextButton
from objects.visual_objects import Base, Pipe
from objects.game_objects import Game

from config.config import *


class View:
    """Parent object"""

    def __init__(self):

        self.active = True
        self.clock = pygame.time.Clock()

        self.replay_button = TextButton(font=REPLAY_BUTTON_FONT,
                                        color=REPLAY_BUTTON_COLOR,
                                        border=True,
                                        center=REPLAY_BUTTON_CENTER,
                                        height=REPLAY_BUTTON_HEIGHT,
                                        width=REPLAY_BUTTON_WIDTH,
                                        text=REPLAY_BUTTON_TEXT)

        self.replay = False

        self.return_button = ImageButton(image=RETURN_BUTTON_IMAGE,
                                         center=RETURN_BUTTON_CENTER,
                                         height=RETURN_BUTTON_HEIGHT,
                                         width=RETURN_BUTTON_WIDTH)

        self.return_start_view = False

        self.base = Base(y=INITIAL_BASE_Y)

        self._initialize_window()

    def _initialize_window(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird AI')

    def run(self):
        while self.active:
            self._main_loop()
            # Redraw window
            self.clock.tick(FPS)
            self._redraw_window()
            pygame.display.update()

    def _main_loop(self):
        for event in pygame.event.get():
            self._manage_event(event)

        # ...

    def _manage_event(self, event):
        if event.type == pygame.QUIT:
            self._quit_window()
        elif event.type == pygame.MOUSEBUTTONUP:
            self._manage_click_events()

        # ...

    def _manage_click_events(self):

        self.mouse_position = pygame.mouse.get_pos()
        self._click_on_return()

        # ...

    def _redraw_window(self):

        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))

        self.base.draw(window=self.window)

        # ...

    def _quit_window(self):
        self.active = False

    def _click_on_return(self):
        if self.return_button.is_under(mouse_position=self.mouse_position):
            self.return_start_view = True
            self._quit_window()

    def _click_on_restart(self):
        if not self.game.active and self.replay_button.is_under(self.mouse_position):
            self.replay = True
            self._quit_window()


class GameView(View):

    def __init__(self):

        super().__init__()

        self.pipes = [Pipe(x=INITIAL_PIPE_X)]

        # ...

    def _main_loop(self):

        super()._main_loop()

        self._manage_collisions()

        self._manage_pipes()

        self._move_objects()

        # ...

    def _manage_click_events(self):

        super()._manage_click_events()
        super()._click_on_restart()

    def _manage_pipes(self):

        # Pipes to remove
        pipes_to_remove = []

        for pipe in self.pipes:
            # If it gets off the screen add it to the list to remove
            if pipe.x + pipe.WIDTH < 0:
                pipes_to_remove.append(pipe)

        for pipe_to_remove in pipes_to_remove:
            self.pipes.remove(pipe_to_remove)

    def _update_score(self, with_bird):
        for pipe in self.pipes:
            # If the pipe is passed create a new one
            if not pipe.passed and pipe.x < with_bird.x:
                pipe.passed = True
                self.pipes.append(Pipe(x=INITIAL_PIPE_X))
                self.game.score += 1

    def _move_objects(self):

        if self.game.active:
            # Base
            self.base.move()
            # Pipes
            for pipe in self.pipes:
                pipe.move()

    def _redraw_window(self):

        super()._redraw_window()

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

        # ...
