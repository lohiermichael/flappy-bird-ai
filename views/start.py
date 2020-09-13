
from objects.visual_objects import Base
from objects.buttons import CollectionRadioButtons
from .view_management.view_template import View

from config.config import *


class StartView(View):

    def __init__(self):
        super().__init__()

        self.name = 'start'

        self.base = Base(y=INITIAL_BASE_Y)

        self.game_type_selection = CollectionRadioButtons(collection_messages=SELECTION_GAME_TYPE_MESSAGES,
                                                          font=SELECTION_GAME_TYPE_FONT,
                                                          width=SELECTION_GAME_TYPE_WIDTH,
                                                          color=SELECTION_GAME_TYPE_COLOR,
                                                          height=SELECTION_GAME_TYPE_HEIGHT,
                                                          center=SELECTION_GAME_TYPE_CENTER)

        self.selected_game_type = None

    def _main_loop(self):

        self._manage_events()

        self._redraw_window()

    def _manage_events(self):

        self.mouse_position = pygame.mouse.get_pos()

        # Hover over an element
        self.game_type_selection.hovered(
            mouse_position=self.mouse_position)

        for event in pygame.event.get():
            # Quite the window
            if event.type == pygame.QUIT:
                self._quit_window()

            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_press()

    def _mouse_press(self):
        for i_button, button in enumerate(self.game_type_selection.list_buttons):
            if button.is_under(self.mouse_position):
                self.game_type_selection.select(i_button)
                self.selected_game_type = button.text
                self._quit_window()

    def _redraw_window(self):
        self.clock.tick(FPS)

        # Window
        self.window.blit(BACKGROUND_IMAGE,
                         (INITIAL_BACKGROUND_X, INITIAL_BACKGROUND_Y))

        # Base
        self.base.draw(window=self.window)

        # Title
        self.window.blit(GAME_TITLE_IMAGE, (GAME_TITLE_X, GAME_TITLE_Y))

        # Game type selection

        self.game_type_selection.draw(window=self.window)

        pygame.display.update()
