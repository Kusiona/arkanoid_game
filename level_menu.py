import pygame
from pygame.surface import Surface
from pygame.transform import scale


class BackgroundLevelMenu(Surface):

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height
        # todo image/level_menu.jpg константа на уровне класса
        self.image = pygame.image.load('images/level_menu.jpg')

    def create_background_image(self):
        self.image = scale(self.image, (self.width, self.height))
        self.blit(self.image, (0, 0))

    def handle_event(self, event):
        pass
