import os

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
