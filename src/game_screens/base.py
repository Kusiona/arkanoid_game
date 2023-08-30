import pygame
from pygame.time import Clock
from src.common.processing_image import Image
# from src.common.buttons import Button


class BaseInterface:
    FONT_PATH = 'static/fonts/InvasionBold.ttf'
    MAIN_COLOR = (25, 25, 112)
    COLOR_SHADOW = (128, 0, 128)

    def __init__(self, width: int, height: int, main_surface, main_app_class):
        self.main_surface = main_surface
        self.main_app_class = main_app_class
        self.width = width
        self.height = height
        self.main_text = None
        self.text_shadow = None
        self.text_x = None
        self.text_y = None
        self.lvl_menu_button = None
        self.exit_button = None

    def create_background_image(self, clock: Clock, fps: int, background_image: Image = None) -> None:
        pass

    def create_text(self, text: str, size: int, coefficient: int) -> None:
        font = pygame.font.Font(self.FONT_PATH, size)
        self.main_text = font.render(text, True, self.MAIN_COLOR)
        self.text_shadow = font.render(text, True, self.COLOR_SHADOW)
        text_width, text_height = font.size(text)
        self.text_x = (self.width - text_width) / 2
        self.text_y = ((self.height / 2) - text_height) / coefficient

    def create_buttons(self, text: str, size: int, coefficient: int, next_screen) -> None:
        font = pygame.font.Font(self.FONT_PATH, size)
        text_size = font.size(text)
        self.text_x = (self.width - text_size[0]) / 2
        self.text_y = self.height - (self.height / coefficient)

        button = Button(text_size=text_size, text_x=self.text_x, text_y=self.text_y, next_screen=next_screen)
        button.create(text=text, font=pygame.font.Font(self.FONT_PATH, size), action=text)
        if text == 'CHOOSE LEVEL':
            self.lvl_menu_button = button
        elif text == 'EXIT' or text == 'BACK':
            self.exit_button = button
        self.main_text = button.button_text
        self.text_shadow = button.button_text_shadow

    def build_interface(self, clock: Clock, fps: int, background_image: Image) -> None:
        pass
