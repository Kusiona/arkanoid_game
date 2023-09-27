import pygame
from pygame.event import Event
from pygame.event import post as post_event
from src.common.base.button import TextButton, ImageButton
from src.game_screens.level import Level


class PlayCompanyButton(TextButton):
    text = 'PLAY COMPANY'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            from src.game_screens.play_company_menu import PlayCompanyMenu
            self.parent_class.main_app_class.current_screen_class = PlayCompanyMenu


class PlayButton(TextButton):
    text = 'PLAY!'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            pass


class LevelsButton(TextButton):
    text = 'CHOOSE LEVEL'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            from src.game_screens.levels_menu import LevelsMenu
            self.parent_class.main_app_class.current_screen_class = LevelsMenu


class ExitButton(TextButton):
    text = 'EXIT'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            post_event(Event(pygame.QUIT))


class LevelsMenuBackButton(TextButton):
    text = 'BACK'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            from src.game_screens.main_menu import MainMenu
            self.parent_class.main_app_class.current_screen_class = MainMenu


class ContinueButton(TextButton):
    text = 'CONTINUE'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            from src.game_screens.level import Level
            self.parent_class.main_app_class.current_screen_class = Level


class ExitMenuButton(TextButton):
    text = 'EXIT TO MENU'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.platform_offset = 0
            self.parent_class.main_app_class.ball_offset_y = 0
            self.parent_class.main_app_class.ball_offset_x = 0
            self.parent_class.main_app_class.life_counter = 3
            self.parent_class.main_app_class.levels_config = None
            self.parent_class.main_app_class.read_levels_config()
            del self.parent_class.main_app_class.block_group
            del self.parent_class.main_app_class.ball_offset_x
            del self.parent_class.main_app_class.ball_offset_y
            del self.parent_class.main_app_class.speed_x
            del self.parent_class.main_app_class.speed_y
            if pygame.K_SPACE in self.parent_class.main_app_class.buttons_presses:
                self.parent_class.main_app_class.buttons_presses.pop(pygame.K_SPACE)
            from src.game_screens.levels_menu import LevelsMenu
            self.parent_class.main_app_class.current_screen_class = LevelsMenu


class AgainButton(TextButton):
    text = 'AGAIN'

    def handle_event(self, event):
        if self.check_left_clicked(event):
            from src.game_screens.level import Level
            self.parent_class.main_app_class.current_screen_class = Level
            self.parent_class.main_app_class.life_counter = 3
            del self.parent_class.main_app_class.block_group


class LevelButton(ImageButton):
    def __init__(self, parent_class, image, level_name):
        super().__init__(parent_class, image)
        self.level_name = level_name

    def handle_event(self, event):
        if pygame.K_SPACE in self.parent_class.main_app_class.buttons_presses:
            self.parent_class.main_app_class.buttons_presses.pop(pygame.K_SPACE)
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.current_level = self.level_name
            self.parent_class.main_app_class.current_screen_class = Level
