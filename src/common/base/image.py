from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite


# вынести сюда в апдейт ресайз картинок из всех мест в приложении
class Image(Sprite):
    IMAGES_DIRECTORY = 'static/images/'

    def __init__(self, filename, source_class=None, width=None, height=None):
        super().__init__()
        self.width = width
        self.height = height
        self.filename = filename
        self.source_class = source_class
        self.image_surface = None
        self.create()
        self.rect = self.image_surface.get_rect()

    def create(self):
        path = self.get_image_path(self.filename)
        self.image_surface = self.read_image(path)
        if self.width and self.height:
            self.scale()

    def get_image_path(self, filename):
        return self.IMAGES_DIRECTORY + filename

    def read_image(self, path):
        return load(path)

    def scale(self, width=None, height=None):
        if width and height:
            self.width, self.height = width, height

        self.image_surface = scale(
            self.image_surface,
            (self.width, self.height)
        )
