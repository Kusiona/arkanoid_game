from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite


class Image(Sprite):
    CONFIG_KEY = 'image'

    def __init__(self, main_app_class, filename, source_class=None, width=None, height=None):
        super().__init__()
        self.width = width
        self.height = height
        self.filename = filename
        self.source_class = source_class
        self.image_surface = None
        self.config = main_app_class.config[self.CONFIG_KEY]
        self.create()
        self.rect = self.image_surface.get_rect()

    def create(self) -> None:
        path = self.get_image_path(self.filename)
        self.image_surface = self.read_image(path)
        if self.width and self.height:
            self.scale()

    def get_image_path(self, filename) -> None:
        return self.config['images_directory'] + filename

    def read_image(self, path):
        return load(path)

    def scale(self, width=None, height=None) -> None:
        if width and height:
            self.width, self.height = width, height

        self.image_surface = scale(
            self.image_surface,
            (self.width, self.height)
        )
