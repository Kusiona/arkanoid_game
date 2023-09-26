from pygame.surface import Surface
from pygame.event import Event
from src.common.buttons import PlayButton, LevelsButton, ExitButton
from src.common.image import Animation
from src.common.base.font import Font
from src.common.base.events import EventHandlingMixin


class MainMenuInterface:
    # дублирование с лвл меню интерфейсом, а теперь еще и с меню паузы, лол
    TITLE_TEXT = 'ARKANOID'
    TITLE_FONT_COEFF = 0.2
    BUTTONS_FONT_COEFF = 0.1

    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.width = parent_class.get_width()
        self.height = parent_class.get_height()
        self.play_button = None
        self.levels_button = None
        self.exit_button = None
        self.render()

    def render(self) -> None:
        self.create_title()
        self.create_buttons()

    def get_font_size(self, coeff):
        size = int(self.width * coeff)
        if self.height < self.width:
            size = int(self.height * coeff)

        return size

    def create_title(self):
        font_size = self.get_font_size(self.TITLE_FONT_COEFF)
        font = Font(self.TITLE_TEXT, font_size)
        text_width, text_height = font.surface.get_width(), font.surface.get_height()
        x = (self.width - text_width) / 2
        y = (self.height / 3) - text_height
        self.parent_class.blit(
            font.shadow_surface,
            (
                font.get_shadow_x(x, font_size),
                font.get_shadow_y(y, font_size),
            )
        )
        self.parent_class.blit(font.surface, (x, y))

    def create_buttons(self):
        font_size = self.get_font_size(self.BUTTONS_FONT_COEFF)
        self.play_button = PlayButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (self.play_button.width / 2)
        y = self.height / 2
        self.play_button.render(x, y)

        self.levels_button = LevelsButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (self.levels_button.width / 2)
        y += font_size * 2
        self.levels_button.render(x, y)

        self.exit_button = ExitButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (self.exit_button.width / 2)
        y += font_size * 2
        self.exit_button.render(x, y)

    def handle_event(self, event):
        pass


class MainMenu(Surface):
    interface_class = MainMenuInterface
    # DYNAMIC = True

    def __init__(self, main_app_class):
        super().__init__((main_app_class.WIDTH, main_app_class.HEIGHT))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
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
