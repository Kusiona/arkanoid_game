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


class LevelIcon(Sprite):

    def __init__(self, width, height, index, icon):
        super().__init__()
        self.index = index
        self.icon = icon
        self.rect = self.icon.get_rect()
        self.image = None
        self.icon_group = Group()
        self.width = width
        self.height = height
        self.icon_x = 0
        self.icon_y = 0

    def update(self, seconds=None):
        width = int(self.width / 5)
        height = int(self.height / 5)
        self.icon = pygame.transform.scale(self.icon, (width, height))
        self.create_coords(icon_width=width, icon_height=height)
        self.rect = self.icon.get_rect(topleft=(self.icon_x, self.icon_y))
        self.image = pygame.Surface((width + 10, height + 10))
        self.image.fill((128, 0, 128))
        self.image.blit(self.icon, (5, 5))

    def create_coords(self, icon_width, icon_height):
        indent_edge_x = (self.width - icon_width * 3.4) / 2
        indent_edge_y = (self.height - icon_height * 3 - icon_height / 2) / 2
        indent_icon_x = (self.width - indent_edge_x * 2) / 18
        indent_icon_y = (self.height - indent_icon_x * 2) / 18
#todo необходимо выявить обую закономерность и свести if к минимуму
        if self.index == 0:
            self.icon_x = indent_edge_x
            self.icon_y = indent_edge_y
        elif self.index == 1:
            self.icon_x = indent_edge_x + icon_width + indent_icon_x
            self.icon_y = indent_edge_y
        elif self.index == 2:
            self.icon_x = indent_edge_x + icon_width*2 + indent_icon_x*2
            self.icon_y = indent_edge_y
        elif self.index == 3:
            self.icon_x = indent_edge_x
            self.icon_y = indent_edge_y + icon_height + indent_icon_y
        elif self.index == 4:
            self.icon_x = indent_edge_x + icon_width + indent_icon_x
            self.icon_y = indent_edge_y + icon_height + indent_icon_y
        elif self.index == 5:
            self.icon_x = indent_edge_x + icon_width*2 + indent_icon_x*2
            self.icon_y = indent_edge_y + icon_height + indent_icon_y
        elif self.index == 6:
            self.icon_x = indent_edge_x
            self.icon_y = indent_edge_y + icon_height*2 + indent_icon_y*2
        elif self.index == 7:
            self.icon_x = indent_edge_x + icon_width + indent_icon_x
            self.icon_y = indent_edge_y + icon_height*2 + indent_icon_y*2
        elif self.index == 8:
            self.icon_x = indent_edge_x + icon_width*2 + indent_icon_x*2
            self.icon_y = indent_edge_y + icon_height*2 + indent_icon_y*2
