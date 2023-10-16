from src.common.base.font import Font
from src.common.base.base_interface import BaseInterface
from src.common.base.base_menu import BaseMenu


class PlayCompanyInterface(BaseInterface):

    def __init__(self, parent_class):
        super().__init__(parent_class)

    def create_title(self):
        indentation = self.height * self.parent_class.config['title_font_coeff']
        for line, phrase in self.parent_class.config['title_text'].items():
            font_size = self.get_font_size(self.parent_class.config['title_font_coeff'])
            font = Font(self.main_app_class, phrase, font_size)
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


class PlayCompanyMenu(BaseMenu):
    CONFIG_KEY = 'play_company_menu'
    interface_class = PlayCompanyInterface

    def __init__(self, main_app_class):
        super().__init__(main_app_class)
