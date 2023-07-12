import pygame
from pygame import image

from pygame.surface import Surface
from pygame.sprite import Sprite, Group
from processing_image import Image


class Level(Surface):

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height

    def collect_level(self, clock, fps, main_surface):
        pass


# todo продумать, как привязать к уровню определенную картинку и вставлять ее в список на экран меню
class LevelSurface(Surface):
    def __init__(self, width, height, clock, fps):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.fps = fps
        self.clock = clock
        self.level_images = [image.load(f'images/images_level/{i}.jpg') for i in range(1, 10)]

    def handle_event(self, event):
        pass


# # todo сделать окантовку вокруг иконки уровня
# # todo объединить создание иконок в группу, чтобы рендерить группу, а не каждую иконку в отдельности

