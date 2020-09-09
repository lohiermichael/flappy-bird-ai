import pygame


class Image:
    def __init__(self, path, scale=False, dimensions=None):
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


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

FPS = 30
GRAVITY_CONSTANT = 9.8

####################### IMAGES #######################

BIRD_IMAGES = {
    'wings_down': Image(path='./img/bird/bird_wings_down.png', scale=2).image,
    'wings_up': Image(path='./img/bird/bird_wings_up.png', scale=2).image,
    'wings_middle': Image(path='./img/bird/bird_wings_middle.png', scale=2).image
}

BACKGROUND_IMAGE = Image(path='./img/background.png',
                         scale=True, dimensions=(600, 900)).image

PIPE_IMAGE = Image(path='./img/pipe.png').image

BASE_IMAGE = Image(path='./img/base.png').image

####################### BIRDS #######################

INITIAL_BIRD_X = 200
INITIAL_BIRD_Y = 200

####################### BACKGROUND #######################

INITIAL_BACKGROUND_X = 0
INITIAL_BACKGROUND_Y = 0
