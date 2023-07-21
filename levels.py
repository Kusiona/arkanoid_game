from pygame import image
from pygame.surface import Surface
import pygame
from pygame.sprite import Sprite
from pygame.transform import scale
from processing_image import Image
from pygame.time import Clock
from pygame.event import Event


class Level(Sprite):

    def __init__(self, width: int, height: int, main_surface, lvl_bg_img: Surface, main_app_class):
        super().__init__()
        self.main_app_class = main_app_class
        self.width = width
        self.height = height
        self.main_surface = main_surface
        self.image = lvl_bg_img
        self.rect = self.image.get_rect()
        self.platform = None
        self.ball = None

    def build_interface(self, clock: Clock, fps: int, background_image: Image) -> None:
        self.platform = Platform(
            width=self.width, height=self.height,
            main_app_class=self.main_app_class
        )
        self.ball = Ball(
            width=self.width, height=self.height,
            main_app_class=self.main_app_class, coord_platform=self.platform.y_coord
        )
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.main_surface.blit(self.image, (0, 0))
        self.main_surface.blit(self.platform.image, self.platform.rect)
        self.main_surface.blit(self.ball.image, self.ball.rect)

    def update(self) -> None:
        self.platform.update()
        self.ball.update()
        self.main_surface.blit(self.platform.image, (self.platform.x_coord, self.platform.y_coord))
        self.main_surface.blit(self.ball.image, (self.ball.x_coord, self.ball.y_coord))


class LevelSurface(Surface):
    interface = Level

    def __init__(self, width: int, height: int, level_number: int, main_app_class):
        super().__init__((width, height))
        self.main_app_class = main_app_class
        self.width = width
        self.height = height
        self.level_number = level_number
        self.level_images = [image.load(f'images/images_level/{i}.jpg') for i in range(1, 10)]
        self.image = self.level_images[self.level_number]
        self.interface = Level(
            width=self.width, height=self.height,
            main_surface=self, lvl_bg_img=self.image,
            main_app_class=self.main_app_class
        )
        self.image.set_alpha(180)

    def handle_event(self, event: Event):
        self.interface.update()

    def __repr__(self):
        return 'LevelSurface'

    def get_name(self):
        return self.__repr__()


class Platform(Sprite):
    IMAGE_PATH = 'images/images_elements/platform.png'

    def __init__(self, width: int, height: int, main_app_class):
        super().__init__()
        self.main_app_class = main_app_class
        self.main_width = width
        self.width = self.main_width / 4
        self.height = height / 30
        self.x_coord = (self.main_width - (self.main_width / 8 * 5)) + self.main_app_class.platform_offset
        self.y_coord = height - (height / 18)
        self.spawn_coords = (self.x_coord, self.y_coord)
        self.image = scale(image.load(self.IMAGE_PATH), (self.width, self.height))
        self.rect = self.image.get_rect(topleft=self.spawn_coords)

    def update(self) -> None:
        if self.main_app_class.platform_move_right:
            if not self.x_coord + self.width + 23 >= self.main_width:
                self.main_app_class.platform_offset += 30
        if self.main_app_class.platform_move_left:
            if not self.x_coord - 23 <= 0:
                self.main_app_class.platform_offset -= 30
        self.rect = self.image.get_rect(topleft=(self.x_coord-1, self.y_coord))


class Ball(Sprite):
    IMAGE_PATH = 'images/images_elements/ball.png'

    def __init__(self, width: int, height: int, main_app_class, coord_platform: float):
        super().__init__()
        self.main_app_class = main_app_class
        self.main_width = width
        self.main_height = height
        self.width = self.main_width / 20
        self.height = self.main_height / 20
        self.platform = self.main_app_class.current_screen.interface.platform
        self.x_coord = self.platform.rect.x + self.platform.width / 2 - self.width / 2
        self.y_coord = self.main_height - (self.main_height - coord_platform) - self.height
        self.spawn_coords = (self.x_coord, self.y_coord)
        self.image = scale(image.load(self.IMAGE_PATH), (self.width, self.height))
        self.rect = self.image.get_rect(topleft=self.spawn_coords)

    def update(self) -> None:
        if self.main_app_class.ball_movement:
            pass


class Block:
    pass
