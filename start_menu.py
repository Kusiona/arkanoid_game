import pygame
import sys
from buttons import Button
from pygame import image
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.transform import scale


class BackgroundImage(Sprite):

    def __init__(self, time_interval):
        super().__init__()
        self.images = [image.load(f'main_menu_animation_images/{i}.gif') for i in range(0, 164)]
        self.index = 0
        self.image = self.images[self.index]
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()

        self.time_interval = time_interval
        self.timer = 0

    def update(self, seconds):

        self.timer += seconds
        if self.index == 164:
            self.index = 0
        if self.timer >= self.time_interval:
            self.image = self.images[self.index]

            if not (self.width, self.height) == self.image.get_size():
                self.image = scale(self.image, (self.width, self.height))

            self.timer = 0


class MainMenuInterface(Surface):
    TEXT = 'ARKANOID'
    main_text = ''
    text_shadow = ''
    text_x = 0
    text_y = 0
    play_text = ''
    play_text_shadow = ''
    exit_text = ''
    exit_text_shadow = ''
    play_button = ''
    exit_button = ''

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height

    def create_text(self):
        font = pygame.font.Font('fonts/InvasionBold.ttf', 130)
        self.main_text = font.render(self.TEXT, True, (25, 25, 112))
        self.text_shadow = font.render(self.TEXT, True, (128, 0, 128))
        text_width, text_height = font.size(self.TEXT)
        self.text_x = (self.width - text_width) / 2
        self.text_y = ((self.height / 2) - text_height) / 2

    def create_play_button(self, text):
        screen = self
        action = text
        text = text
        font = pygame.font.Font('fonts/InvasionBold.ttf', 100)
        text_size = font.size(text)
        self.text_x = (self.width - text_size[0]) / 2
        self.text_y = self.height - (self.height / 2)

        self.play_button = Button(screen=screen,
                                  text=text,
                                  font=font,
                                  text_size=text_size,
                                  text_x=self.text_x,
                                  text_y=self.text_y,
                                  action=action)
        self.play_button.create()
        self.play_text = self.play_button.button_text
        self.play_text_shadow = self.play_button.button_text_shadow

    def create_exit_button(self, text):
        screen = self
        action = text
        text = text
        font = pygame.font.Font('fonts/InvasionBold.ttf', 100)
        text_size = font.size(text)
        self.text_x = (self.width - text_size[0]) / 2
        self.text_y = self.height - (self.height / 4)

        self.exit_button = Button(screen=screen,
                                  text=text,
                                  font=font,
                                  text_size=text_size,
                                  text_x=self.text_x,
                                  text_y=self.text_y,
                                  action=action)
        self.exit_button.create()
        self.exit_text = self.exit_button.button_text
        self.exit_text_shadow = self.exit_button.button_text_shadow


class MainMenuSurface(Surface):

    def __init__(self, width, height, background):
        super().__init__((width, height))
        self.width = width
        self.height = height
        # todo background -> background_image
        self.background = background
        self.main_menu = MainMenuInterface(width=background.width, height=background.height)

    def collect_main_menu(self, clock, fps):
        self.background.width = self.width
        self.background.height = self.height

        seconds = clock.tick(fps) / 300.0
        self.background.update(seconds)
        self.main_menu.create_text()
        self.blit(self.main_menu, (0, 0))
        self.blit(self.background.image, (0, 0))
        self.blit(self.main_menu.main_text, (self.main_menu.text_x, self.main_menu.text_y))
        self.blit(self.main_menu.text_shadow, (self.main_menu.text_x + 5, self.main_menu.text_y + 5))

        self.main_menu.create_play_button('PLAY')
        self.blit(self.main_menu.play_text, (self.main_menu.text_x, self.main_menu.text_y))
        self.blit(self.main_menu.play_text_shadow, (self.main_menu.text_x + 4, self.main_menu.text_y + 4))

        self.main_menu.create_exit_button('EXIT')
        self.blit(self.main_menu.exit_text, (self.main_menu.text_x, self.main_menu.text_y))
        self.blit(self.main_menu.exit_text_shadow, (self.main_menu.text_x + 4, self.main_menu.text_y + 4))
        self.background.index += 1

    def listen_events(self, event):
        if self.main_menu.play_button.collidepoint(event.pos):
            return False
        elif self.main_menu.exit_button.collidepoint(event.pos):
            pygame.quit()
            sys.exit()
