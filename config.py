import pygame
from objects.visual_objects import Image

WIN_WIDTH = 600
WIN_HEIGHT = 800


BIRD_IMAGES = {
    'wings_down': Image(path='./img/bird/bird_wings_down.png', scale=2),
    'wings_up':Image(path='./img/bird/bird_wings_up.png', scale=2),
    'wings_middle': Image(path='./img/bird/bird_wings_middle.png', scale=2)
}

BACKGROUND_IMAGE = Image(path='./img/background.png', scale=True, dimensions=(600, 900))

PIPE_IMAGE = Image(path='./img/pipe.png')

BASE_IMAGE = Image(path='./img/base.png')