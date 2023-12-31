import pygame
from pygame.event import Event
from pygame.event import post as post_event
from src.common.base.button import TextButton, ImageButton
from src.game_screens.level import Level


class PlayCompanyButton(TextButton):
    CONFIG_KEY = 'play_company_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            from src.game_screens.play_company_menu import PlayCompanyMenu
            self.parent_class.main_app_class.current_screen_class = PlayCompanyMenu


class PlayButton(TextButton):
    CONFIG_KEY = 'play_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.company = True
            self.parent_class.main_app_class.level_active = True


class LevelsButton(TextButton):
    CONFIG_KEY = 'levels_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            from src.game_screens.levels_menu import LevelsMenu
            self.parent_class.main_app_class.current_screen_class = LevelsMenu


class ExitButton(TextButton):
    CONFIG_KEY = 'exit_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            post_event(Event(pygame.QUIT))


class BackButton(TextButton):
    CONFIG_KEY = 'back_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            from src.game_screens.main_menu import MainMenu
            self.parent_class.main_app_class.current_screen_class = MainMenu


class ContinueButton(TextButton):
    CONFIG_KEY = 'continue_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            if self.parent_class.main_app_class.company:
                self.parent_class.main_app_class.level_active = True
            from src.game_screens.level import Level
            self.parent_class.main_app_class.current_screen_class = Level


class ExitMenuButton(TextButton):
    CONFIG_KEY = 'exit_menu_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.del_attr()
            self.parent_class.main_app_class.current_level_company = str(1)
            self.parent_class.main_app_class.company = False
            from src.game_screens.levels_menu import LevelsMenu
            self.parent_class.main_app_class.current_screen_class = LevelsMenu


class AgainButton(TextButton):
    CONFIG_KEY = 'again_button'

    def handle_event(self, event) -> None:
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.del_attr()
            from src.game_screens.level import Level
            self.parent_class.main_app_class.current_screen_class = Level


class LevelButton(ImageButton):
    def __init__(self, parent_class, image, level_name):
        super().__init__(parent_class, image)
        self.level_name = level_name

    def handle_event(self, event) -> None:
        if pygame.K_SPACE in self.parent_class.main_app_class.buttons_presses:
            self.parent_class.main_app_class.buttons_presses.pop(pygame.K_SPACE)
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.current_level = self.level_name
            self.parent_class.main_app_class.current_screen_class = Level
