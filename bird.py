import os

import pygame

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25  # Degrees to rotate the bird sprite while moving up and down
    ROTATION_VELOCITY = 20  # How much to the bird rotate each frame
    ANIMATION_TIME = 5  # How long to show a bird animation

    def __init__(self, x, y):
        # (x,y) starting position coordinates
        self.x = x
        self.y = y

        # tilt tells how much the bird image is tilted
        self.tilt = 0

        # tick_count is used for configuring physics of the bird
        self.tick_Count = 0

        # velocity is the velocity of the bird
        self.velocity = 0

        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]  # bird1.png

    def jump(self):
        self.velocity = -10.5
        self.tick_Count = 0
        self.height = self.y

    def move(self):
        self.tick_Count += 1
        displacement = self.velocity * self.tick_Count + 1.5 * self.tick_Count**2

        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        # if the bird is moving upwards then tilt the bird upward
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        # if the bird is moving downwards then tilt the bird downwards
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, win):
        self.image_count += 1

        # To animate the bird flapping its wings...
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMAGES[1]
        elif self.image_count == self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        )

        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
