from pygame import image
import pygame
from pygame.sprite import Sprite, Group
from pygame.transform import scale
from pygame.surface import Surface


class Image(Sprite):

    def __init__(self, time_interval: float = None, width: int = None, height: int = None):
        super().__init__()
        self.images = [image.load(f'main_menu_animation_images/{i}.gif') for i in range(0, 164)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.time_interval = time_interval
        self.timer = 0

    def update(self, seconds: float) -> None:
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

    def create_lvl_menu_bg_img(self) -> None:
        self.image = image.load('images/level_menu.jpg')

    def create_lvl_bg_img(self) -> None:
        pass


class LevelIcon(Sprite):

    def __init__(self, width: int, height: int, index: int, icon: Surface):
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
        # to prevent circular import
        from levels import LevelSurface
        self.next_screen = LevelSurface

    def update(self, seconds: float = None) -> None:
        width = int(self.width / 5)
        height = int(self.height / 5)
        self.icon = pygame.transform.scale(self.icon, (width, height))
        self.create_coords(icon_width=width, icon_height=height)
        self.rect = self.icon.get_rect(topleft=(self.icon_x, self.icon_y))
        self.image = pygame.Surface((width + 10, height + 10))
        self.image.fill((128, 0, 128))
        self.image.blit(self.icon, (5, 5))

    def create_coords(self, icon_width: int, icon_height: int) -> None:
        interval = icon_width / 6
        start_coord_x = (self.width - (icon_width * 3 + interval * 2)) / 2
        start_coord_y = (self.height - (icon_height * 3 + interval * 2)) / 2
        self.icon_x = start_coord_x
        self.icon_y = start_coord_y
        if self.index % 3:
            self.icon_x += icon_width * (self.index % 3) + interval * (self.index % 3)
            if self.index != 2 and self.index != 1:
                self.icon_y += icon_height * (self.index // 3) + interval * (self.index // 3)
        elif not self.index % 3:
            self.icon_y += icon_height * (self.index // 3) + interval * (self.index // 3)
