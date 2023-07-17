from pygame import image
from pygame.surface import Surface
import pygame
from pygame.sprite import Sprite


class Level(Sprite):

    def __init__(self, width, height, main_surface, lvl_bg_img):
        super().__init__()
        self.width = width
        self.height = height
        self.main_surface = main_surface
        self.image = lvl_bg_img
        self.rect = self.image.get_rect()
        self.platform = None

    def build_interface(self, clock, fps, background_image):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.main_surface.blit(self.image, (0, 0))

        self.platform = Platform(width=self.width, height=self.height)
        self.main_surface.blit(self.platform.image, self.platform.rect)

    def update(self):
        pass


class LevelSurface(Surface):
    interface = Level

    def __init__(self, width, height, level_number):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.level_images = [image.load(f'images/images_level/{i}.jpg') for i in range(1, 10)]
        self.image = self.level_images[level_number]
        self.interface = Level(width=self.width, height=self.height, main_surface=self, lvl_bg_img=self.image)
        self.image.set_alpha(180)

    def handle_event(self, event):
        # todo отлавливать события в главном цикле и передавать сюда
        return ('2', None)


class Platform(Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.width = width / 4
        self.height = height / 20
        self.x_coord = width / 2
        self.y_coord = height - (height / 8)
        self.spawn_coords = (self.x_coord, self.y_coord)
        self.image = pygame.transform.scale(pygame.image.load('images/images_elements/platform.png'), (self.width, self.height))
        self.rect = self.image.get_rect(topleft=self.spawn_coords)

    def movement(self):
        pass


class Block:
    pass


class Ball:
    pass
