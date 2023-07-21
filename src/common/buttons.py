from pygame.rect import Rect
import pygame
import sys
from pygame.font import Font


class Button(Rect):
    COLOR = (25, 25, 112)
    SHADOW_COLOR = (128, 0, 128)

    def __init__(self, text_size: tuple, text_x: float = 1, text_y: float = 1, next_screen=None):
        super().__init__(text_x, text_y, text_size[0], text_size[1])
        self.button_text = None
        self.button_text_shadow = None
        self.text = None
        self.font = None
        self.action = None
        self.next_screen = next_screen

    def create(self, text: str, font: Font, action: str) -> None:
        self.text = text
        self.font = font
        self.action = action
        self.button_text = self.font.render(self.text, True, self.COLOR)
        self.button_text_shadow = self.font.render(self.text, True, self.SHADOW_COLOR)

    def exit(self) -> None:
        pygame.quit()
        sys.exit()
