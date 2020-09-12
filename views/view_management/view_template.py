from config.config import *


class View:
    """Parent object"""

    def __init__(self):

        self.active = True
        self.close_window = False
        self.clock = pygame.time.Clock()

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

    def start_main_loop(self):
        while self.active:
            self._main_loop()

    def _main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_window()
        self._redraw_window()
