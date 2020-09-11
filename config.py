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
            self.image = pygame.transform.scale(
                self.image, self.dimensions)

        if reverse:
            self.image = pygame.transform.flip(self.image, False, True)


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

####################### GAME #######################

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FPS = 60
GRAVITY_CONSTANT = 3  # For birds (minus wings flapping)
GAME_SPEED = 5
STAT_FONT = pygame.font.SysFont("comicsans", 40)

# Score
SCORE_FONT = STAT_FONT
SCORE_COLOR = (255, 255, 255)
SCORE_WIDTH = 30
SCORE_HEIGHT = 10


# Game over message
GAME_OVER_WIDTH = 300
GAME_OVER_HEIGHT = 150
GAME_OVER_IMAGE = Image(path='./img/game_over.png',
                        scale=True,
                        dimensions=(GAME_OVER_WIDTH, GAME_OVER_HEIGHT)).image
GAME_OVER_X = 150
GAME_OVER_Y = 300

# Replay button
REPLAY_BUTTON_FONT = pygame.font.SysFont('Comic Sans MS', 30)
REPLAY_BUTTON_COLOR = (0, 0, 0)
REPLAY_BUTTON_CENTER = (WINDOW_WIDTH/2, 450)
REPLAY_BUTTON_WIDTH = 120
REPLAY_BUTTON_HEIGHT = 50
REPLAY_BUTTON_TEXT = 'Replay'


####################### BIRDS #######################

BIRD_IMAGES = {
    'wings_down': Image(path='./img/bird/bird_wings_down.png', scale=2).image,
    'wings_up': Image(path='./img/bird/bird_wings_up.png', scale=2).image,
    'wings_middle': Image(path='./img/bird/bird_wings_middle.png', scale=2).image
}


INITIAL_BIRD_X = 200
INITIAL_BIRD_Y = 200

####################### BACKGROUND #######################

BACKGROUND_IMAGE = Image(path='./img/background.png',
                         scale=True, dimensions=(600, 900)).image


INITIAL_BACKGROUND_X = 0
INITIAL_BACKGROUND_Y = 0


####################### PIPE #######################

PIPE_WIDTH = 80
PIPE_HEIGHT = 400

PIPE_IMAGES = {
    'bottom': Image(path='./img/pipe.png', scale=True, dimensions=(PIPE_WIDTH, PIPE_HEIGHT)).image,
    'top': Image(path='./img/pipe.png', reverse=True, scale=True, dimensions=(PIPE_WIDTH, PIPE_HEIGHT)).image
}

INITIAL_PIPE_X = 700


####################### BASE #######################

BASE_WIDTH = WINDOW_WIDTH
BASE_HEIGHT = 100

BASE_IMAGE = Image(path='./img/base.png', scale=True,
                   dimensions=(BASE_WIDTH, BASE_HEIGHT)).image

INITIAL_BASE_Y = 730
