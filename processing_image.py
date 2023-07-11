from pygame import image
import pygame
from pygame.sprite import Sprite, Group
from pygame.transform import scale
from pygame.rect import Rect


class Image(Sprite):

    def __init__(self, time_interval=None, width=None, height=None):
        super().__init__()
        self.images = [image.load(f'main_menu_animation_images/{i}.gif') for i in range(0, 164)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.time_interval = time_interval
        self.timer = 0
        self.level_bg_images = [image.load(f'images/images_level/{i}.jpg') for i in range(1, 10)]

    def update(self, seconds):
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()

        self.timer += seconds
        if self.index == len(self.images):
            self.index = 0
        if self.timer >= self.time_interval:
            self.image = self.images[self.index]

            if not (self.width, self.height) == self.image.get_size():
                self.image = scale(self.image, (self.width, self.height))

            self.timer = 0
        self.index += 1

    def create_lvl_menu_bg_img(self):
        self.image = image.load('images/level_menu.jpg')

    def create_lvl_bg_img(self):
        pass

    def create_lvl_icon(self, width, height):
        self.image = self.level_bg_images[0]
        self.width = width / 6
        self.height = height / 6
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
