from config.config import *
from objects.buttons import ImageButton, TextButton


class View:
    """Parent object"""

    def __init__(self):

        self.active = True
        self.close_window = False
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

        self.initialize_window()

    def initialize_window(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird AI')

    def _redraw_window(self):
        self.clock.tick(FPS)
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))
        # ...
        pygame.display.update()

    def _quit_window(self):
        self.close_window = False
        self.active = False

    def run_main_loop(self):
        while self.active:
            self._main_loop()

    def _main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_window()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_position = pygame.mouse.get_pos()
                self._press_on_restart()
                self._press_on_return()

    def _press_on_restart(self):
        if not self.game.active and self.replay_button.is_under(self.mouse_position):
            self.replay = True
            self._quit_window()

    def _press_on_return(self):
        if self.return_button.is_under(mouse_position=self.mouse_position):
            self.return_start_view = True
            self._quit_window()
        self._redraw_window()
