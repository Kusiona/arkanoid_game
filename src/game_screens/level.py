import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite, Group
from pygame.event import Event
from src.common.base.image import Image
from src.game_screens.pause import PauseMenu
from src.common.base.font import Font
from src.game_screens.game_over_menu import GameOverMenu


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
                            len_line
                        )
                    )

    def get_block_info(self, map_icon):
        for block_name in self.block_config:
            if ''.join(map_icon) == self.block_config[block_name]['map_icon']:
                return self.block_config[block_name]
            else:
                continue

    def check_block_group(self):
        if not hasattr(self.parent_class.main_app_class, 'block_group'):
            self.parent_class.main_app_class.block_group = Group()
            self.create_block_map()

    def get_font_size(self, coeff):
        size = int(self.width / coeff)
        if self.height < self.width:
            size = int(self.height / coeff)

        return size

    def create_life_counter(self):
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
        self.create_life_counter()
        self.create_platform()
        self.create_ball()
        self.check_block_group()

    def update(self) -> None:
        self.platform.update()
        self.ball.update()
        self.parent_class.main_app_class.block_group.update()
        self.parent_class.blit(self.platform.image, (self.platform.x, self.platform.y))
        self.parent_class.blit(self.ball.image, (self.ball.x, self.ball.y))
        self.parent_class.main_app_class.block_group.draw(self.parent_class)

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

    def restart(self):
        self.main_app_class.buttons_presses.pop(pygame.K_SPACE)
        self.main_app_class.platform_offset = 0
        del self.main_app_class.ball_movement
        self.check_life_counter()

    def check_life_counter(self):
        self.main_app_class.life_counter -= 1
        if self.main_app_class.life_counter == 0:
            del self.main_app_class.block_group
            self.main_app_class.current_screen_class = GameOverMenu

    def check_collisions_ball(self):
        self.check_collisions_ball_wall()
        self.check_collisions_ball_platform()
        self.check_collisions_ball_block()

    def check_collisions_ball_wall(self):
        if self.interface.ball.y - self.interface.ball.padding <= 0:
            self.interface.ball.move_down()
        if self.interface.ball.y + self.interface.ball.padding >= self.main_app_class.HEIGHT:
            self.restart()
        if self.interface.ball.x + self.interface.ball.width + self.interface.ball.padding >= self.main_app_class.WIDTH:
            self.interface.ball.move_left()
        if self.interface.ball.x - self.interface.ball.padding <= 0:
            self.interface.ball.move_right()

    def check_collisions_ball_platform(self):
        if pygame.Rect.colliderect(self.interface.ball.rect, self.interface.platform.rect):
            self.interface.ball.move_up()

    def check_collisions_ball_block(self): # по непонятным мне причинам срабатывает столько раз, сколько живет кубик
        block_collision = pygame.sprite.spritecollideany(
            self.interface.ball, self.main_app_class.block_group
        )
        if block_collision:
            self.interface.ball.move_reverse()
            block_collision.handle_collison()

    def __str__(self):
        return f'Level {self.level_name}'

    def __del__(self):
        if hasattr(self, 'interface'):
            del self.interface
        if hasattr(self, 'background'):
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

    def get_coordinates(self):
        self.count_ball_offset()
        x = self.main_app_class.ball_offset_x
        y = self.main_app_class.ball_offset_y
        return x, y

    def count_ball_offset(self):
        if not pygame.K_SPACE in self.main_app_class.buttons_presses:
            self.main_app_class.ball_offset_x = self.platform.rect.x + self.platform.width / 2 - self.width / 2
            intermediate_result = self.parent_class_height - self.platform.y
            self.parent_class.main_app_class.ball_offset_y = self.parent_class_height - intermediate_result
            self.parent_class.main_app_class.ball_offset_y -= self.height

    def check_attr(self): # переписать
        if not hasattr(self.parent_class.main_app_class, 'ball_offset_x'):
            self.parent_class.main_app_class.ball_offset_x = 0
        if not hasattr(self.parent_class.main_app_class, 'ball_offset_y'):
            self.parent_class.main_app_class.ball_offset_y = 0

        if not hasattr(self.parent_class.main_app_class, 'ball_movement'):
            self.parent_class.main_app_class.ball_movement = {
                                                            'up': True,
                                                            'down': False,
                                                            'right': True,
                                                            'left': False
                                                        }
# ball_movement = {
#     'up-right': {'state': True, 'action': 'x+ y-'},
#     'up-left': {'state': False, 'action': 'x- y-'},
#     'down-right': {'state': False, 'action': 'x+ y+'},
#     'down-left': {'state': False, 'action': 'x- y+'}
# }

    def update(self) -> None:
        if pygame.K_SPACE in self.main_app_class.buttons_presses:
            self.movement_ball()
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def movement_ball(self): #переписать
        if self.parent_class.main_app_class.ball_movement['up']:
            self.parent_class.main_app_class.ball_offset_y -= self.speed
        if self.parent_class.main_app_class.ball_movement['down']:
            self.parent_class.main_app_class.ball_offset_y += self.speed

        if self.parent_class.main_app_class.ball_movement['right']:
            self.parent_class.main_app_class.ball_offset_x += self.speed
        if self.parent_class.main_app_class.ball_movement['left']:
            self.parent_class.main_app_class.ball_offset_x -= self.speed
        self.parent_class.check_collisions_ball()

    def move_reverse(self):
        for move, active in self.parent_class.main_app_class.ball_movement.items():
            self.parent_class.main_app_class.ball_movement[move] = not active

    def move_up(self):
        self.parent_class.main_app_class.ball_movement['up'] = True
        self.parent_class.main_app_class.ball_movement['down'] = False

    def move_down(self):
        self.parent_class.main_app_class.ball_movement['up'] = False
        self.parent_class.main_app_class.ball_movement['down'] = True

    def move_right(self):
        self.parent_class.main_app_class.ball_movement['right'] = True
        self.parent_class.main_app_class.ball_movement['left'] = False

    def move_left(self):
        self.parent_class.main_app_class.ball_movement['right'] = False
        self.parent_class.main_app_class.ball_movement['left'] = True

    def handle_event(self, event):
        pass


class Block(Sprite):
    SIZE_COEFF = 0.7

    def __init__(self, parent_class, block, coord_block_map, len_line):
        super().__init__()
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.parent_class_width = parent_class.get_width()
        self.parent_class_height = parent_class.get_height()
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)

        self.block = block
        self.stoutness = self.block['stoutness']
        self.map_x, self.map_y = coord_block_map
        self.len_line = len_line

        self.width = self.parent_class_width / self.len_line * self.SIZE_COEFF
        self.height = self.parent_class_height / self.len_line * self.SIZE_COEFF / 2

        self.image = Image(self.block['image_path'], self, self.width, self.height).image_surface
        self.x, self.y = self.get_coordinates()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def get_coordinates(self):
        padding_block = self.get_padding_block()
        padding_wall = self.get_padding_wall(padding_block)
        x = padding_wall + (padding_block * self.map_x) + (self.width * self.map_x)
        y = padding_wall + (padding_block * self.map_y) + (self.height * self.map_y)
        return x, y

    def get_padding_block(self):
        return self.width / (self.len_line / 2)

    def get_padding_wall(self, padding_block):
        return (self.parent_class_width - (padding_block * (self.len_line - 1) + self.width * self.len_line)) / 2

    def update(self):
        self.parent_class.blit(self.image, (self.x, self.y))

    def handle_collison(self):
        self.stoutness -= 1
        if not self.stoutness:
            self.kill()

    def handle_event(self, event):
        pass


# todo: на сегодня
#  после уничтожения всех кубиков должен вылезти экран с поздравлением и кнопка выхода в меню уровней
#  у кубиков должны быть "уровни", сделать механику с прозрачностью кубиков на определенном количестве ударов
#  переписать адекватным образом движение мячика, что могло бы упростить работу с столкновением с кубиками
#  остался баг с перекрестом картинок, проверить ссылки на объекты bg
#  при нажатии на пробел в любом экране мячик начинает движение - исправить баг
#
# todo кубики:
#  должны быть контрастыми к фону
#  3 стадии разбития у самого сложного кубика
#
#
#
#

