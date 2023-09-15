import pygame
from pygame.surface import Surface
from src.common.base.font import Font
from src.common.base.image import Image


class GameOverInterface:
    TITLE_TEXT = 'GAME OVER'
    TITLE_FONT_COEFF = 0.12
    BUTTONS_FONT_COEFF = 0.08

    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.width = parent_class.get_width()
        self.height = parent_class.get_height()
        self.exit_menu_button = None
        self.again_button = None
        self.render()

    def render(self):
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
        # to avoid circular imports
        from src.common.buttons import ExitMenuButton, AgainButton
        font_size = self.get_font_size(self.BUTTONS_FONT_COEFF)
        self.again_button = AgainButton(
            parent_class=self.parent_class,
            text_size=font_size
            )
        x = (self.width / 2) - (self.again_button.width / 2)
        y = self.height / 2
        self.again_button.render(x, y)

        self.exit_menu_button = ExitMenuButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (self.exit_menu_button.width / 2)
        y += font_size * 2
        self.exit_menu_button.render(x, y)

    def handle_event(self, event):
        pass


class GameOverMenu(Surface):
    interface_class = GameOverInterface

    def __init__(self, main_app_class):
        super().__init__((main_app_class.WIDTH, main_app_class.HEIGHT))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.render()
        self.interface = self.interface_class(parent_class=self)

    def set_background(self, image):
        self.blit(image, (0, 0))

    def render(self):
        background_exists = hasattr(self.main_app_class, 'background')
        background = self.main_app_class.background if background_exists else None
        filename = 'game_over_menu_bg.jpg'
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
        if hasattr(self, 'background'):
            del self.main_app_class.background
