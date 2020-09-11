from config import *


class Game:
    GAME_OVER_IMAGE = GAME_OVER_IMAGE

    def __init__(self):
        self.score = 0
        self.active = True

    def draw_end_game(self, window, replay_button):

        # Draw game over message
        window.blit(GAME_OVER_IMAGE, (GAME_OVER_X, GAME_OVER_Y))

        # Draw replay button
        replay_button.draw(window=window)


class RectangularButton():
    def __init__(self, font=None, color=None, center=None, border=True, x=None, y=None, height=None, width=None, text=''):
        self.color = color
        self.font = font
        self.border = border

        self.width = width
        self.height = height

        # You can define the position of the button by center...
        if center:
            self.center = center
            self.center_x, self.center_y = self.center
            self.x = self.center_x - int(self.width/2)
            self.y = self.center_y - int(self.height/2)

        # ...or x and y
        if x and y:
            self.x = x
            self.y = y
            self.center = (self.x + int(self.width/2),
                           self.y + int(self.height/2))

        self.text = text

    def draw(self, window, outline=True, outline_thinkness=2, line_width=None):
        """Call this method to draw a button on the screen"""

        if not line_width:
            line_width = 1 if self.border else -1

        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thinkness,
                                               self.y - outline_thinkness,
                                               self.width+outline_thinkness*2,
                                               self.height+outline_thinkness*2), line_width)

        pygame.draw.rect(window, self.color, (self.x,
                                              self.y,
                                              self.width,
                                              self.height), line_width)

        if self.text != '':
            text = self.font.render(self.text, line_width, self.color)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                               self.y + (self.height/2 - text.get_height()/2)))

    def undraw(self, window):
        pygame.draw.rect(window, GREY, (self.x,
                                        self.y,
                                        self.width,
                                        self.height), 0)

    def is_under(self, mouse_position):

        mp_x, mp_y = mouse_position
        return (self.x < mp_x < self.x+self.width) and (self.y < mp_y < self.y+self.height)
