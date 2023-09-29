from pygame.surface import Surface
from src.common.buttons import PlayCompanyButton, LevelsButton, ExitButton
from src.common.image import Animation
from src.common.base.base_interface import BaseInterface


class MainMenuInterface(BaseInterface):

    def __init__(self, parent_class):
        super().__init__(parent_class)

    def create_buttons(self):
        font_size = self.get_font_size(self.parent_class.config['buttons_font_coeff'])
        play_button = PlayCompanyButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (play_button.width / 2)
        y = self.height / 2
        play_button.render(x, y)

        levels_button = LevelsButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (levels_button.width / 2)
        y += font_size * 2
        levels_button.render(x, y)

        exit_button = ExitButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (exit_button.width / 2)
        y += font_size * 2
        exit_button.render(x, y)


class MainMenu(Surface):
    CONFIG_KEY = 'pause_menu'
    interface_class = MainMenuInterface

    def __init__(self, main_app_class):
        super().__init__((main_app_class.WIDTH, main_app_class.HEIGHT))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.config = self.main_app_class.config[self.CONFIG_KEY]
        self.render()
        self.interface = self.interface_class(parent_class=self)

    def render(self):
        background_exists = hasattr(self.main_app_class, 'background')
        background = self.main_app_class.background if background_exists else None
        if not background_exists or background and not background.source_class == str(self):
            self.main_app_class.background = Animation(
                directory='main_menu_animation', parent_class=self
            )
        self.main_app_class.background.update(self)

    def handle_event(self, event):
        pass

    def __str__(self):
        return 'MainMenu'

    def __del__(self):
        if hasattr(self, 'interface'):
            del self.interface
