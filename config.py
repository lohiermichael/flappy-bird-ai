import pygame


class Image:
    def __init__(path, scale, dimensions=None):
        self.path = path
        self.scale = scale

        self.image = pygame.load(self.path)
        if not scale: 
            pass
        elif scale == 2:
            self.image = pygame.transform.scale2x(self.image)
        else: # Scale is True
            self.image = pygame.transform.scale(self.image, self.image_dimensions)

        return self.image



WIN_WIDTH = 600
WIN_HEIGHT = 800

GRAVITY_CONSTANT = 9.8


BIRD_IMAGES = {
    'wings_down': Image(path='./img/bird/bird_wings_down.png', scale=2),
    'wings_up':Image(path='./img/bird/bird_wings_up.png', scale=2),
    'wings_middle': Image(path='./img/bird/bird_wings_middle.png', scale=2)
}

BACKGROUND_IMAGE = Image(path='./img/background.png', scale=True, dimensions=(600, 900))

PIPE_IMAGE = Image(path='./img/pipe.png')

BASE_IMAGE = Image(path='./img/base.png')