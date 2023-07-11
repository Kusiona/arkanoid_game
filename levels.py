import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite
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
        self.icon_x = None
        self.icon_y = None
        self.level_icon = None

    def get_level_icon(self, main_surface):
        self.icon_x = self.width / 7
        self.icon_y = self.height / 4
        self.level_icon = Image(width=self.width, height=self.height)
        self.level_icon.create_lvl_icon(width=self.width, height=self.height)
        main_surface.blit(self.level_icon.image, (self.icon_x, self.icon_y))

    def handle_event(self, event):
        pass
        # if self.level_icon.image.collidepoint(event.pos):


# # todo сделать окантовку вокруг иконки уровня
# # todo объединить создание иконок в группу, чтобы рендерить группу, а не каждую иконку в отдельности

