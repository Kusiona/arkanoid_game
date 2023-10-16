import sys
import json
import pygame
from src.game_screens.main_menu import MainMenu
from src.common.base.image import Image
from src.game_screens.level import Level
from src.game_screens.level_complete_menu import LevelCompleteMenu


class Arkanoid:
    CONFIG_KEY = 'main'
    WIDTH = 700
    HEIGHT = 800
    FPS = 30
    extra_event_handlers = []

    def __init__(self):
        self.config = None
        self.read_config()

        pygame.display.set_caption(self.config[self.CONFIG_KEY]['caption'])
        pygame.display.set_icon(pygame.image.load(self.config[self.CONFIG_KEY]['image_path']))
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.levels_config = None
        self.read_levels_config()

        self.current_screen_class = MainMenu
        self.current_screen = self.current_screen_class(self)
        self.buttons_presses = {}

        self.life_counter = 3

        self.company = False
        self.level_active = False
        self.current_level_company = str(1)

    def read_levels_config(self):
        with open('levels_config.json', 'r') as f:
            self.levels_config = json.loads(f.read())

        for level_name, config in self.levels_config.items():
            filename = self.levels_config[level_name]['background_image']
            self.levels_config[level_name]['background_image'] = Image(filename)
            self.levels_config[level_name]['background_image_thumb'] = Image(filename)

    def read_config(self):
        with open('config.json', 'r') as f:
            self.config = json.loads(f.read())

    def track_buttons_presses(self, event):
        target_types = (
            pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
            pygame.KEYDOWN, pygame.KEYUP
        )
        up_types = pygame.MOUSEBUTTONUP, pygame.KEYUP, pygame.BUTTON_WHEELUP
        mouse_types = pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.BUTTON_WHEELDOWN

        if event.type in target_types:
            value = True
            if event.type in up_types:
                value = False

            event_key = event.button if event.type in mouse_types else event.key
            self.buttons_presses[event_key] = value

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        self.track_buttons_presses(event)

        if event.type == pygame.WINDOWRESIZED:
            self.WIDTH = event.x
            self.HEIGHT = event.y

        # подумать как сделать обработку ивентов производительно
        # проверить и узнать удаляются ли у нас все обьекты, не копятся ли за каждый кадр
        # сделать так чтобы каждый класс записывал не только ивент хендлер главному классу но и ивент матчер
        # в цикле мы не будем итерировать все ивенты и давать всему приложению доступ к каждому ивенту поскольку это очень хуево для производительности
        # в цикле мы будем итерироватьсяч по ивент матчером и если матчится, то давать исполнится соответствующему ивент хендлеру
        for event_handler in self.extra_event_handlers:
            event_handler(event)

    def run_game_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update_display()

    def play_main_company(self):
        self.current_level = self.current_level_company

        if int(self.current_level) > 9:
            self.current_screen_class = LevelCompleteMenu
            self.company = False
            self.level_active = False

        if self.level_active:
            self.current_screen_class = Level

        if hasattr(self, 'block_group') and not self.block_group:
            self.del_attr()

    def update_display(self) -> None:
        del self.current_screen

        if self.company:
            self.play_main_company()

        self.extra_event_handlers = []
        self.current_screen = self.current_screen_class(main_app_class=self)
        self.screen.blit(self.current_screen, (0, 0))
        pygame.display.update()

    def del_attr(self):
        self.life_counter = 3
        self.levels_config = None
        self.read_levels_config()
        if hasattr(self, 'block_group'):
            del self.block_group
            del self.platform_offset
            del self.ball_offset_x
            del self.ball_offset_y
            del self.speed_x
            del self.speed_y

        if pygame.K_SPACE in self.buttons_presses:
            self.buttons_presses.pop(pygame.K_SPACE)

        self.level_active = False

        # import sys
        # from src.game_screens.level import Ball, Platform, Block
        # print(f'{self.current_screen_class} references count', sys.getrefcount(self.current_screen_class))
        # print('Ball references count', sys.getrefcount(Ball))
        # print('Platform references count', sys.getrefcount(Platform))
        # print('Block references count', sys.getrefcount(Block))

"""
посмотреть дает ли такой подход какие-то бонусы
if event.type == VIDEORESIZE:
    screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
    
и вот такой подход через сингл груп и дроу
block = pygame.sprite.Sprite()
block.image = pygame.transform.scale(img, (64, 64))
block.rect = block.image.get_rect()

group = pygame.sprite.GroupSingle(block)

while True:
    #TODO: event handling
    group.draw(screen)
    pygame.display.update()


подумать как обеспечить возможность блитать классы обертки напрямую а не обращаясь к их атрибутам для этого

узнать даст ли нам какие то бонусы трансформ smoothscale

продумать общий стиль названий и использования методов render и create

"""
if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
