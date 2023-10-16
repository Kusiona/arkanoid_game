import sys
import json
import pygame
from src.game_screens.main_menu import MainMenu
from src.common.base.image import Image
from src.game_screens.level import Level
from src.game_screens.level_complete_menu import LevelCompleteMenu


class Arkanoid:
    CONFIG_KEY = 'main'
    extra_event_handlers = []

    def __init__(self):
        self.config = None
        self.read_config()

        pygame.display.set_caption(self.config[self.CONFIG_KEY]['caption'])
        pygame.display.set_icon(pygame.image.load(self.config[self.CONFIG_KEY]['image_path']))
        pygame.mixer.music.load(self.config[self.CONFIG_KEY]['music_path'])
        pygame.mixer.music.play(-1)

        self.width = self.config[self.CONFIG_KEY]['width']
        self.height = self.config[self.CONFIG_KEY]['height']
        self.fps = self.config[self.CONFIG_KEY]['fps']

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.levels_config = None
        self.read_levels_config()

        self.current_screen_class = MainMenu
        self.current_screen = self.current_screen_class(self)
        self.buttons_presses = {}

        self.life_counter = 3

        self.company = False
        self.level_active = False
        self.current_level_company = '1'

    def read_levels_config(self):
        with open('levels_config.json', 'r') as f:
            self.levels_config = json.loads(f.read())

        for level_name, config in self.levels_config.items():
            filename = self.levels_config[level_name]['background_image']
            self.levels_config[level_name]['background_image'] = Image(self, filename)
            self.levels_config[level_name]['background_image_thumb'] = Image(self, filename)

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
            self.width = event.x
            self.height = event.y

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


if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
