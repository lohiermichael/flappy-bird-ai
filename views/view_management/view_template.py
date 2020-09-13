from objects.buttons import ImageButton, TextButton
from objects.visual_objects import Base

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
