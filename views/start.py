from objects.visual_objects import Base
from objects.buttons import CollectionRadioButtons
from .view_management.view_template import View

from config.config import *


class StartView(View):
    def __init__(self):
        super().__init__()

        self.name = "start"

        self.game_type_selection = CollectionRadioButtons(
            collection_messages=SELECTION_GAME_TYPE_MESSAGES,
            font=SELECTION_GAME_TYPE_FONT,
            width=SELECTION_GAME_TYPE_WIDTH,
            color=SELECTION_GAME_TYPE_COLOR,
            height=SELECTION_GAME_TYPE_HEIGHT,
            center=SELECTION_GAME_TYPE_CENTER,
        )

        self.selected_game_type = None

    def _main_loop(self):
        super()._main_loop()

        self.mouse_position = pygame.mouse.get_pos()

        # Hover over an element
        self.game_type_selection.hovered(mouse_position=self.mouse_position)

    def _manage_click_events(self):
        super()._manage_click_events()

        # Click on selection game
        for i_button, button in enumerate(self.game_type_selection.list_buttons):
            if button.is_under(self.mouse_position):
                self.game_type_selection.select(i_button)
                self.selected_game_type = button.text
                self._quit_window()

    def _redraw_window(self):
        super()._redraw_window()

        # Title
        self.window.blit(GAME_TITLE_IMAGE, (GAME_TITLE_X, GAME_TITLE_Y))

        # Game type selection
        self.game_type_selection.draw(window=self.window)
