import pygame
from pygame.event import Event
from pygame.event import post as post_event
from src.common.base.button import TextButton, ImageButton
from src.game_screens.level import Level


class PlayButton(TextButton):
    text = 'PLAY COMPANY'

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


class LevelButton(ImageButton):
    def __init__(self, parent_class, image, level_name):
        super().__init__(parent_class, image)
        self.level_name = level_name

    def handle_event(self, event):
        if self.check_left_clicked(event):
            self.parent_class.main_app_class.current_level = self.level_name
            self.parent_class.main_app_class.current_screen_class = Level
