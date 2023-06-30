import pygame
from pygame.surface import Surface
from pygame.transform import scale


class BackgroundLevelMenu(Surface):

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height
        # todo image/level_menu.jpg константа на уровне класса
        self.image = pygame.image.load('image/level_menu.jpg')

    # todo create_back_image -> create_background_image or create_bg_image  or create_bg_img
    def create_back_image(self):
        self.image = scale(self.image, (self.width, self.height))
        self.blit(self.image, (0, 0))

    def listen_events(self, event):
        print(123)
