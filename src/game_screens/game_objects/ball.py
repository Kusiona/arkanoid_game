import pygame
from pygame.sprite import Sprite
from src.common.base.image import Image
import random


class Ball(Sprite):
    IMAGE_PATH = 'level_elements/ball.png'
    SIZE_COEFF = 0.05
    PADDING_COEFF = 0.03

    def __init__(self, parent_class, speed):
        super().__init__()
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.parent_class_width = parent_class.get_width()
        self.parent_class_height = parent_class.get_height()
        self.width = self.parent_class_width * self.SIZE_COEFF
        self.height = self.parent_class_height * self.SIZE_COEFF
        self.platform = self.parent_class.main_app_class.platform
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)
        self.image = Image(self.IMAGE_PATH, self, self.width, self.height).image_surface
        self.speed = speed
        self.padding = (self.parent_class_height * self.PADDING_COEFF)
        self.check_attr()
        self.x, self.y = self.get_coordinates()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def check_attr(self):
        if not hasattr(self.parent_class.main_app_class, 'ball_offset_x'):
            self.parent_class.main_app_class.ball_offset_x = 0

        if not hasattr(self.parent_class.main_app_class, 'ball_offset_y'):
            self.parent_class.main_app_class.ball_offset_y = 0

        if not hasattr(self.parent_class.main_app_class, 'speed_x'):
            self.parent_class.main_app_class.speed_x = self.speed

        if not hasattr(self.parent_class.main_app_class, 'speed_y'):
            self.parent_class.main_app_class.speed_y = self.speed

    def get_coordinates(self):
        self.count_ball_offset()
        x = self.main_app_class.ball_offset_x
        y = self.main_app_class.ball_offset_y
        return x, y

    def count_ball_offset(self):
        if not pygame.K_SPACE in self.main_app_class.buttons_presses:
            self.main_app_class.ball_offset_x = self.platform.rect.x + (
                    self.platform.width / 2 - self.width / 2)
            self.parent_class.main_app_class.ball_offset_y = self.parent_class_height - (
                    self.parent_class_height - self.platform.y
            ) - self.height

    def update(self) -> None:
        if pygame.K_SPACE in self.main_app_class.buttons_presses:
            self.movement_ball()
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.random_start()

    def random_start(self):
        if random.randint(0, 1):
            self.parent_class.main_app_class.speed_x *= -1

    def movement_ball(self):
        collision = self.parent_class.check_collisions_ball()

        if self.main_app_class.buttons_presses.get(pygame.K_LEFT) and collision and\
                self.parent_class.main_app_class.speed_x < 0:
            self.change_direction_x()

        if self.main_app_class.buttons_presses.get(pygame.K_RIGHT) and collision and\
                self.parent_class.main_app_class.speed_x > 0:
            self.change_direction_x()

        self.check_attr()
        self.parent_class.main_app_class.ball_offset_x -= self.parent_class.main_app_class.speed_x
        self.parent_class.main_app_class.ball_offset_y -= self.parent_class.main_app_class.speed_y

    def change_direction_x(self):
        self.play_sound()
        self.parent_class.main_app_class.speed_x *= -1

    def change_direction_y(self):
        self.play_sound()
        self.parent_class.main_app_class.speed_y *= -1

    def play_sound(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound('static/music/ball_sound.mp3'))

    def handle_event(self, event):
        pass
