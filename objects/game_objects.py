from .visual_objects import RectangularButton

from config.config import *


class Game:
    def __init__(self):
        self.score = 0
        self.active = True

    def draw_score(self, window):
        score_text = f'Score: {self.score}'

        score_label = SCORE_FONT.render(score_text, 1, SCORE_COLOR)

        window.blit(score_label, (SCORE_X, SCORE_Y))


class GamePlay(Game):
    GAME_OVER_IMAGE = GAME_OVER_IMAGE

    def __init__(self):
        super().__init__()

    def draw_end_game(self, window, replay_button):

        # Draw game over message
        window.blit(GAME_OVER_IMAGE, (GAME_OVER_X, GAME_OVER_Y))

        # Draw replay button
        replay_button.draw(window=window)


class GameTrainAI(Game):
    def __init__(self):
        super().__init__()
        self.generation = -1
        self.best_score = 0

        self.total_birds = 0
        self.living_birds = 0

    def draw_generation(self, window):
        generation_text = f'Generation: {self.generation}'

        genration_label = GENERATION_FONT.render(
            generation_text, 1, GENERATION_COLOR)

        window.blit(genration_label, (GENERATION_X, GENERATION_Y))

    def draw_birds_count(self, window):
        birds_count_text = f'Birds count: {self.living_birds}/{self.total_birds}'

        birds_count_label = BIRDS_COUNT_FONT.render(
            birds_count_text, 1, BIRDS_COUNT_COLOR)

        window.blit(birds_count_label, (BIRDS_COUNT_X, BIRDS_COUNT_Y))
