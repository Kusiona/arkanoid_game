from pygame.surface import Surface
from src.common.base.image import Image
from src.common.base.font import Font
from src.common.base.base_interface import BaseInterface


class PlayCompanyInterface(BaseInterface):

    def __init__(self, parent_class):
        super().__init__(parent_class)

    def create_title(self):
        indentation = self.height * self.parent_class.config['title_font_coeff']
        for line, phrase in self.parent_class.config['title_text'].items():
            font_size = self.get_font_size(self.parent_class.config['title_font_coeff'])
            font = Font(phrase, font_size)
            text_width, text_height = font.surface.get_width(), font.surface.get_height()
            x = (self.width - text_width) / 2
            y = indentation * int(line)
            self.parent_class.blit(
                font.shadow_surface,
                (
                    font.get_shadow_x(x, font_size),
                    font.get_shadow_y(y, font_size),
                )
            )
            self.parent_class.blit(font.surface, (x, y))

    def create_buttons(self):
        # to avoid circular imports
        from src.common.buttons import BackButton, PlayButton

        font_size = self.get_font_size(self.parent_class.config['buttons_font_coeff'])

        play_button = PlayButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (play_button.width / 2)
        y = self.height / 2 + font_size * 2
        play_button.render(x, y)

        exit_menu_button = BackButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (exit_menu_button.width / 2)
        y += font_size * 2
        exit_menu_button.render(x, y)


class PlayCompanyMenu(Surface):
    CONFIG_KEY = 'play_company_menu'
    interface_class = PlayCompanyInterface

    def __init__(self, main_app_class):
        super().__init__((main_app_class.WIDTH, main_app_class.HEIGHT))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.config = self.main_app_class.config[self.CONFIG_KEY]
        self.render()
        self.interface = self.interface_class(parent_class=self)
        self.set_alpha(100)

    def set_background(self, image):
        self.blit(image, (0, 0))

    def render(self):
        background_exists = hasattr(self.main_app_class, 'background')
        background = self.main_app_class.background if background_exists else None
        filename = self.config['filename']
        if not background_exists or background and not background.source_class == str(self):
            self.main_app_class.background = Image(
                filename, source_class=str(self),
                width=self.get_width(), height=self.get_height()
            )
        self.set_background(self.main_app_class.background.image_surface)

    def handle_event(self, event):
        pass

    def __del__(self):
        if hasattr(self, 'interface'):
            del self.interface
        if hasattr(self.main_app_class, 'background'):
            del self.main_app_class.background
