import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite


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

    def create_level_icon(self, main_surface):
        pass
        # self.width = self.width / 10
        # self.height = self.height / 10
        # icon_level = BackgroundLevelImage(width=self.width, height=self.height)
        # icon_level.create_icon()
        # main_surface.blit(icon_level.image, (0, 0))

    def handle_event(self, event):
        pass


class BackgroundLevelImage(Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load('images/image_level/sun.png')
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height

    def create_icon(self):
        self.width = self.width / 10
        self.height = self.height / 10
