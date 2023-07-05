import pygame
import sys
from buttons import Button
from pygame import image
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.transform import scale


class BackgroundImage(Sprite):

    def __init__(self, time_interval, width, height):
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


class MainMenuInterface(Surface):

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.main_text = None
        self.text_shadow = None
        self.text_x = None
        self.text_y = None
        self.play_button = None
        self.exit_button = None

    def create_text(self, text):
        font = pygame.font.Font('fonts/InvasionBold.ttf', 130)
        self.main_text = font.render(text, True, (25, 25, 112))
        self.text_shadow = font.render(text, True, (128, 0, 128))
        text_width, text_height = font.size(text)
        self.text_x = (self.width - text_width) / 2
        self.text_y = ((self.height / 2) - text_height) / 2

    def create_button(self, text, coefficient):
        font = pygame.font.Font('fonts/InvasionBold.ttf', 100)
        text_size = font.size(text)
        self.text_x = (self.width - text_size[0]) / 2
        self.text_y = self.height - (self.height / coefficient)

        button = Button(screen=self,
                        text=text,
                        font=pygame.font.Font('fonts/InvasionBold.ttf', 100),
                        text_size=text_size,
                        text_x=self.text_x,
                        text_y=self.text_y,
                        action=text)
        if text == 'PLAY':
            self.play_button = button
        elif text == 'EXIT':
            self.exit_button = button
        self.main_text = button.button_text
        self.text_shadow = button.button_text_shadow


class MainMenuSurface(Surface):
    def __init__(self, width, height, background):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.background_image = background
        self.main_menu = MainMenuInterface(width=self.width, height=self.height)

    def collect_main_menu(self, clock, fps):

        self.main_menu.width = self.width
        self.main_menu.height = self.height

        seconds = clock.tick(fps) / 300.0

        self.background_image.update(seconds)
        self.main_menu.create_text(text='ARKANOID')

        self.blit(self.main_menu, (0, 0))
        self.blit(self.background_image.image, (0, 0))
        self.blit(self.main_menu.main_text, (self.main_menu.text_x, self.main_menu.text_y))
        self.blit(self.main_menu.text_shadow, (self.main_menu.text_x + 5, self.main_menu.text_y + 5))

        self.main_menu.create_button(text='PLAY', coefficient=2)
        self.blit(self.main_menu.main_text, (self.main_menu.text_x, self.main_menu.text_y))
        self.blit(self.main_menu.text_shadow, (self.main_menu.text_x + 4, self.main_menu.text_y + 4))

        self.main_menu.create_button(text='EXIT', coefficient=4)
        self.blit(self.main_menu.main_text, (self.main_menu.text_x, self.main_menu.text_y))
        self.blit(self.main_menu.text_shadow, (self.main_menu.text_x + 4, self.main_menu.text_y + 4))

    def handle_event(self, event):
        if self.main_menu.play_button.collidepoint(event.pos):
            return '2'
        elif self.main_menu.exit_button.collidepoint(event.pos):
            pygame.quit()
            sys.exit()
        return '1'
