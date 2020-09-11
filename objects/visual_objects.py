import os
from random import randint

from config import *


class Bird:
    """Bird class representing the flappy bird"""

    MAX_ROTATION = 25
    IMAGES = BIRD_IMAGES
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 3
    VERTICAL_INERTIA_HEIGHT = 30
    MAX_ANGLE_DOWN = -90
    MAX_TILT_DOWN = -80
    EXTRA_JUMP = -3
    HEIGHT = IMAGES['wings_middle'].get_height()

    def __init__(self, x, y):
        """Initialize the bird object

        Args:
            x (int): Starting x position of the bird (top left corner)
            y (int): Starting y position of the bird (top left corner)
        """

        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.velocity = 0
        self.start_jump_height = self.y
        self.image_count = 0
        self.image = self.IMAGES['wings_up']

    def jump(self):
        """Make the bird jump"""

        self.velocity = -10.5  # To change to make the bird jump more or less quickly
        self.tick_count = 0  # Count of time since we last pressed the jump button
        self.start_jump_height = self.y

    def move(self):
        """
            Make the bird move up and down
            depending on the values set in the jump method
        """

        self.tick_count += 1

        displacement = 0.5 * GRAVITY_CONSTANT * \
            (self.tick_count)**2 + self.velocity * self.tick_count

        # Terminal velocity
        displacement = min(displacement, 16)

        # Extra jump
        if displacement < 0:
            displacement -= self.EXTRA_JUMP

        self.y = self.y + displacement

        # Tilt up: moving up or moving down with inertia
        if displacement < 0 or self.y < self.start_jump_height + self.VERTICAL_INERTIA_HEIGHT:
            self.tilt = max(self.MAX_ROTATION, self.tilt)

        # Tilt down
        else:
            if self.tilt > self.MAX_ANGLE_DOWN:
                self.tilt -= self.ROTATION_VELOCITY
            pass

    def draw(self, window):
        """Draw the bird

        Args:
            window : Pygame window
        """

        self.image_count += 1

        # Animate the bird
        if self.image_count <= self.ANIMATION_TIME:
            self.image = self.IMAGES['wings_up']
        elif self.image_count <= self.ANIMATION_TIME*2:
            self.image = self.IMAGES['wings_middle']
        elif self.image_count <= self.ANIMATION_TIME*3:
            self.image = self.IMAGES['wings_down']
        elif self.image_count <= self.ANIMATION_TIME*4:
            self.image = self.IMAGES['wings_middle']
        elif self.image_count == self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES['wings_up']
            self.image_count = 0

        # Make the bird not flap when it is nose diving
        if self.tilt <= self.MAX_TILT_DOWN:
            self.image = self.IMAGES['wings_middle']
            self.image_count = self.ANIMATION_TIME*2

        blit_rotate_center(window=window,
                           image=self.image,
                           top_left=(self.x, self.y),
                           angle=self.tilt)

    def collide_pipe(self, pipe):
        """The bird collides a pipe

        Args:
            pipe (Pipe): a pipe

        Returns:
            bool: if it collides or not
        """

        # Bird mask
        self.mask = pygame.mask.from_surface(self.image)
        # Pipe masks
        pipe_bottom_mask, pipe_top_mask = pipe.get_masks()

        offset_with_bottom = (round(self.x - pipe.x),
                              round(self.y - pipe.y_bottom))
        offset_with_top = (round(self.x - pipe.x),
                           round(self.y - pipe.y_top))

        collision_bottom_points = self.mask.overlap(
            pipe_bottom_mask, offset_with_bottom)
        collision_top_points = self.mask.overlap(
            pipe_top_mask, offset_with_top)

        if collision_top_points or collision_bottom_points:
            return True

        return False

    def collide_base(self, base):
        """The bird collides a base

        Args:
            base (Base): a base

        Returns:
            bool: if it collides or not
        """

        if self.y + self.HEIGHT > base.y:
            return True
        return False


def blit_rotate_center(window, image, top_left, angle):
    """Rotate a surface and blit it to the window

    Args:
        window : Window to blit
        image : The image surface to rotate
        top_left : The top left position of the image
        angle (float): The angle of rotation
    """

    # Tilt the bird
    rotated_image = pygame.transform.rotate(image, angle)
    # Rotate around the center
    new_rectangle = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rectangle.topleft)


class Pipe:
    """Pipe class representing a pipe (top and bottom)"""

    # Gap between the top and the bottom parts
    GAP = 200
    VELOCITY = GAME_SPEED
    IMAGES = PIPE_IMAGES
    HEIGHT = IMAGES['top'].get_height()
    WIDTH = IMAGES['top'].get_width()

    # img_height = 320
    # img_height * 2 + gap = 840
    MIN_HEIGHT = -200
    MAX_HEIGHT = 0

    def __init__(self, x):
        """Initialize Pipe object

        Args:
            x (int): x-coordinate
        """

        self.x = x

        self.passed = False

        self.top_height = randint(self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.y_top = self.top_height + self.HEIGHT
        self.y_bottom = self.y_top + self.GAP

    def move(self):
        """Move the pipe based on velocity
        """
        self.x -= self.VELOCITY

    def draw(self, window):
        """Draw the top and the bottom part of the pipe

        Args:
            window : Pygame window
        """

        window.blit(self.IMAGES['top'], (self.x, self.top_height))
        window.blit(self.IMAGES['bottom'], (self.x, self.y_bottom))

    def get_masks(self):
        """Get the mask of the top part and the bottom part of the pipeline"""
        bottom_mask = pygame.mask.from_surface(self.IMAGES['bottom'])
        top_mask = pygame.mask.from_surface(self.IMAGES['top'])
        return bottom_mask, top_mask


class Base:
    """Base class representing base floor"""

    VELOCITY = GAME_SPEED
    IMAGE = BASE_IMAGE
    WIDTH = IMAGE.get_width()

    def __init__(self, y):
        """Initialize Base object

        Args:
            y (int): y-coordinate
        """

        self.y = y

        # Two images
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Move the floor so it looks like scrolling"""
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        """Draw the base floor

        Args:
            window : Pygame window
        """

        window.blit(self.IMAGE, (self.x1, self.y))
        window.blit(self.IMAGE, (self.x2, self.y))
