import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.event import Event
from src.common.base.image import Image
from src.game_screens.pause import PauseMenu


class LevelInterface(Sprite):
    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)
        self.width = parent_class.get_width()
        self.height = parent_class.get_height()
        levels_config = self.parent_class.main_app_class.levels_config
        self.image = levels_config[self.parent_class.level_name]['background_image']
        self.image.image_surface.set_alpha(180)
        self.rect = self.image.image_surface.get_rect()
        self.platform = None
        self.ball = None
        self.config = self.parent_class.config
        self.create()

    def create_platform(self):
        self.platform = Platform(self.parent_class, self.config['platform_speed'])
        self.parent_class.blit(self.platform.image, self.platform.rect)

    def create_ball(self):
        self.ball = Ball(parent_class=self.parent_class)
        self.parent_class.blit(self.ball.image, self.ball.rect)

    def create(self):
        self.create_platform()
        self.create_ball()

    def update(self) -> None:
        self.platform.update()
        self.ball.update()
        self.parent_class.blit(self.platform.image, (self.platform.x, self.platform.y))
        self.parent_class.blit(self.ball.image, (self.ball.x, self.ball.y))

    def handle_event(self, event):
        pass


class Level(Surface):
    interface_class = LevelInterface
    # DYNAMIC = True

    def __init__(self, main_app_class):
        super().__init__((main_app_class.WIDTH, main_app_class.HEIGHT))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.level_name = self.main_app_class.current_level
        self.config = self.main_app_class.levels_config[self.level_name]
        self.interface = self.interface_class(parent_class=self)
        self.render()

    def set_background(self, image):
        self.blit(image, (0, 0))

    def render(self):
        bg_image = self.config['background_image']
        screen_size = self.main_app_class.WIDTH, self.main_app_class.HEIGHT
        if (bg_image.width, bg_image.height) != screen_size:
            bg_image.scale(*screen_size)
        self.set_background(bg_image.image_surface)
        self.interface.update()

    def handle_event(self, event: Event):
        # отслеживать window resized
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.main_app_class.current_screen_class = PauseMenu

    def __str__(self):
        return f'Level {self.level_name}'


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


class Ball(Sprite):
    IMAGE_PATH = 'level_elements/ball.png'
    SIZE_COEFF = 0.05

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class
        self.parent_class_width = parent_class.get_width()
        self.parent_class_height = parent_class.get_height()
        self.width = self.parent_class_width * self.SIZE_COEFF
        self.height = self.parent_class_height * self.SIZE_COEFF
        self.platform = self.parent_class.main_app_class.platform
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)
        self.image = Image(self.IMAGE_PATH, self, self.width, self.height).image_surface

        self.x, self.y = self.get_coordinates()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def get_coordinates(self):
        x = self.platform.rect.x + self.platform.width / 2 - self.width / 2
        y = self.parent_class_height - (self.parent_class_height - self.platform.y) - self.height
        return x, y

    def update(self) -> None:
        pass

    def handle_event(self, event):
        pass


class Block:
    def __init__(self):
        pass

    def handle_event(self, event):
        pass
