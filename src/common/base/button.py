import pygame
from pygame.rect import Rect
from src.common.base.font import Font


class BaseButton(Rect):

    def __init__(self, parent_class):
        super().__init__(0, 0, 0, 0)
        self.parent_class = parent_class
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)
        self.config = self.parent_class.main_app_class.config['buttons']

    def check_left_clicked(self, event) -> bool:
        mouse_left_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        if mouse_left_click and self.collidepoint(event.pos):
            return True

        return False

    def create(self) -> None:
        pass

    def render(self, x, y) -> None:
        pass

    def handle_event(self, event) -> None:
        pass


class TextButton(BaseButton):
    CONFIG_KEY = 'base_button'

    def __init__(self, parent_class, text_size):
        super().__init__(parent_class)
        self.button_text = None
        self.text_size = text_size
        self.config = self.config[self.CONFIG_KEY]
        self.create()

    def create(self) -> None:
        self.button_text = Font(self.parent_class.main_app_class, self.config, self.text_size)
        self.width = self.button_text.surface.get_width()
        self.height = self.button_text.surface.get_height()

    def render(self, x, y) -> None:
        self.parent_class.blit(
            self.button_text.shadow_surface,
            (
                self.button_text.get_shadow_x(x, self.text_size),
                self.button_text.get_shadow_y(y, self.text_size)
            )
        )
        text_rect = self.parent_class.blit(self.button_text.surface, (x, y))
        self.update(text_rect)


class ImageButton(BaseButton):
    def __init__(self, parent_class, image):
        super().__init__(parent_class)
        self.image = image
        self.create()

    def create(self) -> None:
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def render(self, x, y) -> None:
        image_rect = self.parent_class.blit(self.image, (x, y))
        self.update(image_rect)
