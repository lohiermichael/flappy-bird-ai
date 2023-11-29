from config.config import *


class Button:
    def __init__(self, center=None, x=None, y=None, height=None, width=None):
        self.width = width
        self.height = height

        if center:
            self.center = center
            self.center_x, self.center_y = self.center
            self.x = self.center_x - int(self.width/2)
            self.y = self.center_y - int(self.height/2)

        if x and y:
            self.x = x
            self.y = y
            self.center = (self.x + int(self.width/2),
                           self.y + int(self.height/2))

    def is_under(self, mouse_position):
        mp_x, mp_y = mouse_position
        return (self.x < mp_x < self.x+self.width) and (self.y < mp_y < self.y+self.height)


class ImageButton(Button):
    def __init__(self, image=None, **kwargs):
        super().__init__(**kwargs)
        self.image = image

    def draw(self, window):
        # Draw game over message
        window.blit(self.image, (self.x, self.y))


class TextButton(Button):
    def __init__(self, font=None, color=None, border=True, text='', **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.font = font
        self.border = border
        self.text = text

    def draw(self, window, outline=True, outline_thickness=2, line_width=None):
        """Call this method to draw a button on the screen"""

        if not line_width:
            line_width = 1 if self.border else -1

        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thickness,
                                               self.y - outline_thickness,
                                               self.width+outline_thickness*2,
                                               self.height+outline_thickness*2), line_width)

        pygame.draw.rect(window, self.color, (self.x,
                                              self.y,
                                              self.width,
                                              self.height), line_width)

        if self.text != '':
            text = self.font.render(self.text, line_width, self.color)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                               self.y + (self.height/2 - text.get_height()/2)))


class CollectionRadioButtons:
    """Multiple circular buttons and some text with it"""

    def __init__(self,
                 collection_messages=None,
                 font=None, color=BLACK,
                 width=None,
                 height=None,
                 center=None,
                 orientation='vertical'):

        self.color = color
        self.width = width
        self.height = height
        self.collection_messages = collection_messages
        self.font = font
        self.orientation = orientation

        self.center = center
        self.center_x, self.center_y = self.center

        self.x = self.center_x - int(self.width/2)
        self.y = self.center_y - int(self.height/2)

        self.list_buttons = self._define_buttons()

        self.selected_button = None

    def _define_buttons(self):

        self.number_buttons = len(self.collection_messages)

        if self.orientation == 'horizontal':
            self.width_button = int(self.width/self.number_buttons)
            self.height_button = self.height

            return [
                RectangularButton(font=self.font,
                                  color=self.color,
                                  border=False,
                                  x=self.x + i_button * self.width_button,
                                  y=self.y,
                                  width=self.width_button,
                                  height=self.height_button,
                                  text=self.collection_messages[i_button])
                for i_button in range(self.number_buttons)
            ]

        elif self.orientation == 'vertical':
            self.width_button = self.width
            self.height_button = int(self.height/self.number_buttons)

            return [
                TextButton(font=self.font,
                           color=self.color,
                           border=False,
                           x=self.x,
                           y=self.y + i_button * self.height_button,
                           width=self.width_button,
                           height=self.height_button,
                           text=self.collection_messages[i_button])
                for i_button in range(self.number_buttons)
            ]

    def draw(self, window):

        for button in self.list_buttons:
            button.draw(window=window, outline=False)

    def is_under(self, mouse_position, index_button):

        button = self.list_buttons[index_button]
        mp_x, mp_y = mouse_position
        return (button.x < mp_x < button.x+button.width) and (button.y < mp_y < button.y+button.height)

    def select(self, index_button):
        self.list_buttons[index_button].border = True

    def hovered(self, mouse_position):
        for i_hovered_button, hovered_button in enumerate(self.list_buttons):
            if hovered_button.is_under(mouse_position):
                hovered_button.border = True
                for i_other_button, other_button in enumerate(self.list_buttons):
                    if not (i_other_button == i_hovered_button or other_button == self.selected_button):
                        other_button.border = False
