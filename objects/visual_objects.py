import os
from config import *


class Bird:
    """Bird class representing the flappy bird"""

    MAX_ROTATION = 25
    IMAGES = BIRD_IMAGES
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5
    VERTICAL_INERTIA_HEIGHT = 50

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
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES['wings_up']

    def jump(self):
        """Make the bird jump"""

        self.velocity = 10.5  # To change to make the bird jump more or less quickly
        self.tick_count = 0  # Count of time since we last pressed the jump button
        self.start_jump_height = self.y

    def move(self):
        """
            Make the bird move up and down
            depending on the values set in the jump method
        """

        displacement = 0.5 * GRAVITY_CONSTANT * \
            (self.tick_count)**2 + self.velocity * self.tick_count

        # TODO Check if needed
        #   # terminal velocity
        # if displacement >= 16:
        #     displacement = (displacement/abs(displacement)) * 16

        # if displacement < 0:
        #     displacement -= 2

        self.y = self.y + displacement

        # Tilt up: moving up or moving down with inertia
        if displacement < 0 or self.y < self.start_jump_height + self.VERTICAL_INERTIA_HEIGHT:
            self.tilt = self.MAX_ROTATION
        # Tilt dow
        else:
            self.tilt = self.tilt + self.ROTATION_VELOCITY

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
        if self.tilt <= -80:
            self.image = self.IMAGES['wings_middle']
            self.image_count = self.ANIMATION_TIME*2

        blit_rotate_center(window=window,
                           image=self.image,
                           top_left=(self.x, self.y),
                           angle=self.tilt)


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
