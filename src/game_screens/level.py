import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite, Group
from pygame.event import Event
from src.common.base.image import Image
from src.game_screens.pause import PauseMenu
from src.common.base.font import Font
from src.game_screens.level_complete_menu import LevelCompleteMenu
from src.game_screens.game_over_menu import GameOverMenu
import random


class LevelInterface(Sprite):
    COUNT_FONT_SIZE_COEFF = 9

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
        self.block_config = self.config['block']
        self.create()

    def create_platform(self):
        self.platform = Platform(self.parent_class, self.config['platform_speed'])

    def create_ball(self):
        self.ball = Ball(parent_class=self.parent_class, speed=self.config['ball_speed'])

    def create_block_map(self):
        len_column = len(self.config['block_map'])
        for y, block_line in enumerate(self.config['block_map']):
            len_line = len(block_line)
            for x, map_icon in enumerate(block_line):
                if map_icon:
                    block = self.get_block_info(map_icon)
                    coord_block_map = (x, y)
                    self.parent_class.main_app_class.block_group.add(
                        Block(
                            self.parent_class,
                            block,
                            coord_block_map,
                            len_line,
                            len_column,
                            self.width,
                            self.height
                        )
                    )

    def get_block_info(self, stoutness):
        for block_name in self.block_config:
            if stoutness == self.block_config[block_name]['stoutness']:
                return self.block_config[block_name]

    def check_block_group(self):
        if not hasattr(self.parent_class.main_app_class, 'block_group'):
            self.parent_class.main_app_class.block_group = Group()
            self.create_block_map()

    def get_font_size(self, coeff):
        size = int(self.width / coeff)
        if self.height < self.width:
            size = int(self.height / coeff)

        return size

    def update_life_counter(self):
        font_size = self.get_font_size(self.COUNT_FONT_SIZE_COEFF)
        font = Font(str(self.parent_class.main_app_class.life_counter), font_size)
        text_width, text_height = font.surface.get_width(), font.surface.get_height()
        x = self.width - text_width * 2
        y = self.height - text_height
        self.parent_class.blit(
            font.shadow_surface,
            (
                font.get_shadow_x(x, font_size),
                font.get_shadow_y(y, font_size),
            )
        )
        self.parent_class.blit(font.surface, (x, y))

    def create(self):
        self.create_platform()
        self.create_ball()
        self.check_block_group()

    def update(self) -> None:
        self.update_life_counter()
        self.platform.update()
        self.ball.update()
        self.parent_class.main_app_class.block_group.update()
        self.parent_class.blit(self.platform.image, (self.platform.x, self.platform.y))
        self.parent_class.blit(self.ball.image, (self.ball.x, self.ball.y))
        self.parent_class.main_app_class.block_group.draw(self.parent_class)

    def handle_event(self, event):
        if event.type == pygame.WINDOWRESIZED:
            self.width, self.height = event.x, event.y
            self.parent_class.main_app_class.block_group.empty()
            self.create_block_map()


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

    def restart(self):
        self.main_app_class.buttons_presses.pop(pygame.K_SPACE)
        self.main_app_class.platform_offset = 0
        self.check_life_counter()

    def check_level_complete(self):
        if not self.main_app_class.block_group:
            self.main_app_class.current_screen_class = LevelCompleteMenu

    def check_life_counter(self):
        self.main_app_class.life_counter -= 1
        if self.main_app_class.life_counter == 0:
            self.main_app_class.current_screen_class = GameOverMenu

    def check_collisions_ball(self):
        self.check_collisions_ball_wall()
        self.check_collisions_ball_platform()
        self.check_collisions_ball_block()

    def check_collisions_ball_wall(self):
        if self.interface.ball.y - self.main_app_class.speed_y <= 0:
            self.interface.ball.change_direction_y()
        elif self.interface.ball.x + (
                self.interface.ball.width - self.main_app_class.speed_x) >= self.main_app_class.WIDTH:
            self.interface.ball.change_direction_x()
        elif self.interface.ball.x - self.main_app_class.speed_x <= 0:
            self.interface.ball.change_direction_x()
        elif self.interface.ball.y + self.interface.ball.height >= self.main_app_class.HEIGHT:
            self.restart()

    def check_collisions_ball_platform(self):
        if self.interface.ball.rect.colliderect(self.interface.platform.rect):
            self.interface.ball.change_direction_y()

    def check_collisions_ball_block(self):
        block_collision = pygame.sprite.spritecollideany(
            self.interface.ball, self.main_app_class.block_group
        )
        if block_collision:
            if random.randint(0, 1):
                self.interface.ball.change_direction_y()

            else:
                self.interface.ball.change_direction_x()
                self.interface.ball.change_direction_y()
            block_collision.handle_collision()
        self.check_level_complete()

    def handle_event(self, event: Event):
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.main_app_class.current_screen_class = PauseMenu

    def __str__(self):
        return 'Level'

    def __del__(self):
        if hasattr(self, 'interface'):
            del self.interface
        if hasattr(self.main_app_class, 'background'):
            del self.main_app_class.background


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
            self.main_app_class.ball_offset_x = self.platform.rect.x + self.platform.width / 2 - self.width / 2
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
        self.parent_class.check_collisions_ball()
        self.parent_class.main_app_class.ball_offset_x -= self.parent_class.main_app_class.speed_x
        self.parent_class.main_app_class.ball_offset_y -= self.parent_class.main_app_class.speed_y

    def change_direction_x(self):
        self.parent_class.main_app_class.speed_x *= -1

    def change_direction_y(self):
        self.parent_class.main_app_class.speed_y *= -1

    def handle_event(self, event):
        pass


class Block(Sprite):
    inner_indent_coeff = 0.01
    outer_indent_coeff = 0.04

    def __init__(self, parent_class, block,
                 coord_block_map, len_line, len_column,
                 parent_class_width, parent_class_height):
        super().__init__()
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.parent_class_width = parent_class_width
        self.parent_class_height = parent_class_height
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)

        self.block = block
        self.stoutness = self.block['stoutness']
        self.map_x, self.map_y = coord_block_map
        self.len_line = len_line
        self.len_column = len_column
        self.width = self.get_width()
        self.height = self.get_height()

        self.image = Image(self.block['image_path'], self, self.width, self.height).image_surface
        self.x, self.y = self.get_coordinates()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def get_coordinates(self):
        x = self.get_outer_indent_x() + (self.get_inner_indent_x() * self.map_x) + (self.width * self.map_x)
        y = self.get_outer_indent_y() + (self.get_inner_indent_y() * self.map_y) + (self.height * self.map_y)
        return x, y

    def get_outer_indent_x(self):
        return self.parent_class_width * self.outer_indent_coeff

    def get_outer_indent_y(self):
        return self.parent_class_height * self.outer_indent_coeff

    def get_inner_indent_x(self):
        return self.parent_class_width * self.inner_indent_coeff

    def get_inner_indent_y(self):
        return self.parent_class_height * self.inner_indent_coeff

    def get_available_width(self):
        available_width = self.parent_class_width - (
                self.get_outer_indent_x() * 2) - (self.get_inner_indent_x() * (self.len_line - 1))
        if available_width < 0:
            available_width = 0
        return available_width

    def get_available_height(self):
        available_height = (self.parent_class_height / 2) - (
                self.get_outer_indent_y() * 2) - (self.get_inner_indent_y() * (self.len_column - 1))
        if available_height < 0:
            available_height = 0
        return available_height

    def get_width(self):
        if self.get_available_width():
            return self.get_available_width() / self.len_line
        else:
            return 0

    def get_height(self):
        return self.get_available_height() / self.len_column

    def update(self):
        self.parent_class.blit(self.image, (self.x, self.y))

    def handle_collision(self):
        self.stoutness -= 1
        self.parent_class.config['block_map'][self.map_y][self.map_x] = self.stoutness
        if not self.stoutness:
            self.kill()
        else:
            self.image = Image(
                f'level_elements/{self.stoutness}_stoutness_block.jpg',
                self, self.width,
                self.height
            ).image_surface

    def handle_event(self, event):
        pass
