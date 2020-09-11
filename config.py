import pygame


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


GAME_SPEED = 5

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

FPS = 30
GRAVITY_CONSTANT = 3  # For birds (minus wings flapping)


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

PIPE_IMAGES = {
    'bottom': Image(path='./img/pipe.png').image,
    'top': Image(path='./img/pipe.png', reverse=True).image
}

INITIAL_PIPE_X = 500


####################### BASE #######################

BASE_WIDTH = WINDOW_WIDTH
BASE_HEIGHT = 100

BASE_IMAGE = Image(path='./img/base.png', scale=True,
                   dimensions=(BASE_WIDTH, BASE_HEIGHT)).image

INITIAL_BASE_Y = 730
