import pygame
from pygame.sprite import Sprite
from src.common.base.image import Image


class Platform(Sprite):
    IMAGE_PATH = 'level_elements/platform.png'
    WIDTH_COEFF = 0.25
    HEIGHT_COEFF = 0.03
    PADDING_COEFF = 0.03

    def __init__(self, parent_class, speed):
        super().__init__()
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.parent_class_width = parent_class.get_width()
        self.parent_class_height = parent_class.get_height()
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)
        self.speed = speed

        self.width = self.parent_class_width * self.WIDTH_COEFF
        self.height = self.parent_class_height * self.HEIGHT_COEFF

        if not hasattr(self.parent_class.main_app_class, 'platform_offset'):
            self.parent_class.main_app_class.platform_offset = 0

        self.x, self.y = self.get_coordinates()

        self.image = Image(self.IMAGE_PATH, self, self.width, self.height).image_surface
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.parent_class.main_app_class.platform = self

    def get_coordinates(self):
        x = ((self.parent_class_width / 2) - (self.width / 2)) + self.main_app_class.platform_offset
        y = self.parent_class_height - self.height - (self.parent_class_height * self.PADDING_COEFF)
        return x, y

    def update(self) -> None:
        buttons_presses = self.main_app_class.buttons_presses
        pressed_k_left = buttons_presses.get(pygame.K_LEFT)
        pressed_k_right = buttons_presses.get(pygame.K_RIGHT)
        padding = (self.parent_class_height * self.PADDING_COEFF)
        # разобраться почему отступ по боками не такой же как и снизу
        if pressed_k_right:
            if not self.x + self.width + padding >= self.parent_class_width:
                self.main_app_class.platform_offset += self.speed
        if pressed_k_left:
            if not self.x - padding <= 0:
                self.main_app_class.platform_offset -= self.speed
        self.rect = self.image.get_rect(topleft=(self.x - 1, self.y))

    def handle_event(self, event):
        pass
