from pygame.surface import Surface
from src.common.base.base_interface import BaseInterface
from src.common.base.image import Image


class BaseMenu(Surface):
    CONFIG_KEY = ''
    interface_class = BaseInterface

    def __init__(self, main_app_class):
        super().__init__((main_app_class.width, main_app_class.height))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.config = self.main_app_class.config[self.CONFIG_KEY]
        self.render()
        self.interface = self.interface_class(parent_class=self)

    def render(self) -> None:
        background_exists = hasattr(self.main_app_class, 'background')
        background = self.main_app_class.background if background_exists else None
        filename = self.config['filename']
        if not background_exists or background and not background.source_class == str(self):
            self.main_app_class.background = Image(
                self.main_app_class,
                filename, source_class=str(self),
                width=self.get_width(), height=self.get_height()
            )
        self.set_background(self.main_app_class.background.image_surface)

    def set_background(self, image) -> None:
        self.blit(image, (0, 0))

    def handle_event(self, event) -> None:
        pass

    def __del__(self) -> None:
        if hasattr(self, 'interface'):
            del self.interface
        if hasattr(self.main_app_class, 'background'):
            del self.main_app_class.background
