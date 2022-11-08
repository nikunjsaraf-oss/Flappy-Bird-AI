# import libraries
import pygame
import neat
import time
import os
import random

# Screen dimension
WIN_WIDTH = 500
WIN_HEIGHT = 800
FPS = 30

# Load Sprites
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)
BASE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png"))
)
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png"))
)


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
            d -= 2

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


class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - self.bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - self.bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point:
            return True
        return False


class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))


def draw_window(win, bird):
    win.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()


main()
