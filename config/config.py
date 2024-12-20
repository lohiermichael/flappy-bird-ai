import pygame

pygame.font.init()


class Image:
    def __init__(self, path, scale=False, dimensions=None, reverse=False):
        self.path = path
        self.scale = scale
        self.dimensions = dimensions

        self.image = pygame.image.load(self.path)
        if not scale:
            pass
        elif scale == 2:
            self.image = pygame.transform.scale2x(self.image)
        else:  # Scale is True
            self.image = pygame.transform.scale(self.image, self.dimensions)

        if reverse:
            self.image = pygame.transform.flip(self.image, False, True)


####################### GAME #######################


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FPS = 30
GRAVITY_CONSTANT = 3  # For birds (minus wings flapping)
GAME_SPEED = 20
STAT_FONT = pygame.font.SysFont("comicsans", 40)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Return button
RETURN_BUTTON_WIDTH = 120
RETURN_BUTTON_HEIGHT = 100
RETURN_BUTTON_IMAGE = Image(
    path="img/return.png",
    scale=True,
    dimensions=(RETURN_BUTTON_WIDTH, RETURN_BUTTON_HEIGHT),
).image
RETURN_BUTTON_CENTER = ((9 / 10) * WINDOW_WIDTH, (1 / 20) * WINDOW_HEIGHT)
RETURN_BUTTON_TEXT = "Replay"


##### Start view #####

# Title
GAME_TITLE_IMAGE = Image(path="./img/start_game/game_title.png").image
GAME_TITLE_X = (1 / 4) * WINDOW_WIDTH
GAME_TITLE_Y = (1 / 10) * WINDOW_HEIGHT

# Selection game type radio buttons
SELECTION_GAME_TYPE_MESSAGES = [
    "Play Normal Game",
    "Play Against AI",
    "Train AI",
    "Test AI",
]
SELECTION_GAME_TYPE_FONT = pygame.font.SysFont("Comic Sans MS", 30)
SELECTION_GAME_TYPE_COLOR = WHITE
SELECTION_GAME_TYPE_WIDTH = (1 / 2) * WINDOW_WIDTH
SELECTION_GAME_TYPE_HEIGHT = (1 / 4) * WINDOW_HEIGHT
SELECTION_GAME_TYPE_CENTER = ((1 / 2) * WINDOW_WIDTH, (1 / 2) * WINDOW_HEIGHT)


##### Play view #####

# Score
SCORE_FONT = STAT_FONT
SCORE_COLOR = WHITE
SCORE_X = 30
SCORE_Y = 10


# Game over message
GAME_OVER_WIDTH = 300
GAME_OVER_HEIGHT = 150
GAME_OVER_IMAGE = Image(
    path="./img/end_game/play/game_over.png",
    scale=True,
    dimensions=(GAME_OVER_WIDTH, GAME_OVER_HEIGHT),
).image
GAME_OVER_X = 150
GAME_OVER_Y = 300

# Replay button
REPLAY_BUTTON_FONT = pygame.font.SysFont("Comic Sans MS", 30)
REPLAY_BUTTON_COLOR = BLACK
REPLAY_BUTTON_CENTER = (WINDOW_WIDTH / 2, 450)
REPLAY_BUTTON_WIDTH = 120
REPLAY_BUTTON_HEIGHT = 50
REPLAY_BUTTON_TEXT = "Replay"

##### Train AI view #####

# Generation
GENERATION_FONT = STAT_FONT
GENERATION_COLOR = (255, 255, 255)
GENERATION_X = 30
GENERATION_Y = 35

# Birds Count
BIRDS_COUNT_FONT = STAT_FONT
BIRDS_COUNT_COLOR = WHITE
BIRDS_COUNT_X = 30
BIRDS_COUNT_Y = 60

# Best score
BEST_SCORE_FONT = STAT_FONT
BEST_SCORE_COLOR = WHITE
BEST_SCORE_X = int(WINDOW_WIDTH / 5)
BEST_SCORE_Y = int(WINDOW_HEIGHT / 2)

#### Play against AI ####

# You won
YOU_WON_WIDTH = 300
YOU_WON_HEIGHT = 150
YOU_WON_IMAGE = Image(
    path="./img/end_game/against_ai/you_won.png",
    scale=True,
    dimensions=(YOU_WON_WIDTH, YOU_WON_HEIGHT),
).image
YOU_WON_X = 150
YOU_WON_Y = 300

# AI won
AI_WON_WIDTH = 300
AI_WON_HEIGHT = 150
AI_WON_IMAGE = Image(
    path="./img/end_game/against_ai/ai_won.png",
    scale=True,
    dimensions=(AI_WON_WIDTH, AI_WON_HEIGHT),
).image
AI_WON_X = 150
AI_WON_Y = 300


####################### BIRDS #######################

PLAYER_BIRD_IMAGES = {
    "wings_down": Image(path="./img/bird/player/bird_wings_down.png", scale=2).image,
    "wings_up": Image(path="./img/bird/player/bird_wings_up.png", scale=2).image,
    "wings_middle": Image(
        path="./img/bird/player/bird_wings_middle.png", scale=2
    ).image,
}

AI_BIRD_IMAGES = {
    "wings_down": Image(path="./img/bird/ai/bird_wings_down.png", scale=2).image,
    "wings_up": Image(path="./img/bird/ai/bird_wings_up.png", scale=2).image,
    "wings_middle": Image(path="./img/bird/ai/bird_wings_middle.png", scale=2).image,
}


INITIAL_BIRD_X = 200
INITIAL_BIRD_Y = 300

####################### BACKGROUND #######################

BACKGROUND_IMAGE = Image(
    path="./img/background.png", scale=True, dimensions=(600, 900)
).image


INITIAL_BACKGROUND_X = 0
INITIAL_BACKGROUND_Y = 0


####################### PIPE #######################

PIPE_WIDTH = 80
PIPE_HEIGHT = 400

PIPE_IMAGES = {
    "bottom": Image(
        path="./img/pipe.png", scale=True, dimensions=(PIPE_WIDTH, PIPE_HEIGHT)
    ).image,
    "top": Image(
        path="./img/pipe.png",
        reverse=True,
        scale=True,
        dimensions=(PIPE_WIDTH, PIPE_HEIGHT),
    ).image,
}

INITIAL_PIPE_X = 700


####################### BASE #######################

BASE_WIDTH = WINDOW_WIDTH
BASE_HEIGHT = 100

BASE_IMAGE = Image(
    path="./img/base.png", scale=True, dimensions=(BASE_WIDTH, BASE_HEIGHT)
).image

INITIAL_BASE_Y = 730
