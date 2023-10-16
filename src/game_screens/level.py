import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite, Group
from pygame.event import Event
from src.game_screens.pause_menu import PauseMenu
from src.common.base.font import Font
from src.game_screens.level_complete_menu import LevelCompleteMenu
from src.game_screens.game_over_menu import GameOverMenu
from src.game_screens.game_objects.platform import Platform
from src.game_screens.game_objects.ball import Ball
from src.game_screens.game_objects.block import Block
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
            if self.main_app_class.company:
                self.main_app_class.current_level_company = str(int(self.main_app_class.current_level_company) + 1)
            else:
                self.main_app_class.current_screen_class = LevelCompleteMenu

    def check_life_counter(self):
        self.main_app_class.life_counter -= 1
        if self.main_app_class.life_counter == 0:
            self.main_app_class.current_screen_class = GameOverMenu
            if self.main_app_class.company:
                self.main_app_class.company = False

    def check_collisions_ball(self):
        self.check_collisions_ball_wall()
        self.check_collisions_ball_block()
        return self.check_collisions_ball_platform()

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
        if pygame.Rect.collidepoint(self.interface.ball.rect, self.interface.platform.rect.topleft) or \
                pygame.Rect.collidepoint(self.interface.ball.rect, self.interface.platform.rect.topright):
            self.interface.ball.change_direction_y()
            return True

        if pygame.Rect.collidepoint(self.interface.ball.rect, self.interface.platform.rect.bottomleft) or \
                pygame.Rect.collidepoint(self.interface.ball.rect, self.interface.platform.rect.bottomright):
            self.interface.ball.change_direction_y()
            return True

        if self.interface.ball.rect.colliderect(self.interface.platform.rect):
            self.interface.ball.change_direction_y()
            return True
        return False

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
            self.main_app_class.level_active = False
            self.main_app_class.current_screen_class = PauseMenu

    def __str__(self):
        return 'Level'

    def __del__(self):
        if hasattr(self, 'interface'):
            del self.interface

        if hasattr(self.main_app_class, 'background'):
            del self.main_app_class.background
