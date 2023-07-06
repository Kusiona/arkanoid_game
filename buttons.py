from pygame.rect import Rect
import pygame
import sys


class Button(Rect):
    COLOR = (25, 25, 112)
    SHADOW_COLOR = (128, 0, 128)

    def __init__(self, text_size, text_x=1, text_y=1):
        super().__init__(text_x, text_y, text_size[0], text_size[1])
        self.screen = None
        self.button_text = None
        self.button_text_shadow = None
        self.text = None
        self.font = None
        self.action = None

    def create(self, screen, text, font, action):
        self.screen = screen
        self.text = text
        self.font = font
        self.action = action
        self.button_text = self.font.render(self.text, True, self.COLOR)
        self.button_text_shadow = self.font.render(self.text, True, self.SHADOW_COLOR)

    def exit(self):
        pygame.quit()
        sys.exit()


