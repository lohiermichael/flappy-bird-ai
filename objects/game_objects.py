from config import *


class Game:
    GAME_OVER_IMAGE = GAME_OVER_IMAGE

    def __init__(self):
        self.score = 0
        self.active = True

    def draw_game_over(self, window):
        window.blit(GAME_OVER_IMAGE, (GAME_OVER_X, GAME_OVER_Y))
