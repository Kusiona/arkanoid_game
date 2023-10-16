from src.common.base.font import Font


class BaseInterface:
    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.width = parent_class.get_width()
        self.height = parent_class.get_height()
        self.render()

    def render(self) -> None:
        self.create_title()
        self.create_buttons()

    def get_font_size(self, coeff) -> int:
        size = int(self.width * coeff)
        if self.height < self.width:
            size = int(self.height * coeff)
        return size

    def create_title(self) -> None:
        font_size = self.get_font_size(self.parent_class.config['title_font_coeff'])
        font = Font(self.main_app_class, self.parent_class.config['title_text'], font_size)
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

    def create_buttons(self) -> None:
        pass

    def handle_event(self, event) -> None:
        pass
