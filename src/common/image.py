from src.common.base.image import Image, scale
from pygame import Surface


class Animation:
    TIME_INTERVAL = 0.25
    ANIMATION_DELAY = 150
    FRAMES_FILE_FORMAT = 'gif'

    def __init__(self, directory, parent_class):
        self.parent_class = parent_class
        self.source_class = str(parent_class)
        self.clock = self.parent_class.main_app_class.clock
        self.fps = self.parent_class.main_app_class.FPS
        self.directory = directory
        self.images = self.read_images()
        self.image = self.images[0]
        self.index = 1
        self.timer = 0

    def read_image(self, filename, width, height):
        return Image(filename, width=width, height=height)

    def read_images(self):
        images = []
        for idx in range(0, 164):
            images.append(self.read_image(
                f'{self.directory}/{idx}.{self.FRAMES_FILE_FORMAT}',
                *self.parent_class.get_size()
            ))

        return images

    def update(self, parent_class) -> None:
        self.parent_class = parent_class
        seconds = self.clock.tick(self.fps) / self.ANIMATION_DELAY
        self.timer += seconds

        if self.index == len(self.images):
            self.index = 0

        if self.timer >= self.TIME_INTERVAL:
            next_image = self.images[self.index]
            next_image_size = next_image.image_surface.get_size()
            if not next_image_size == self.parent_class.get_size():
                next_image.image_surface = scale(
                    next_image.image_surface,
                    self.parent_class.get_size()
                )
            self.image = next_image
            self.timer = 0

        self.index += 1
        self.render_frame()

    def render_frame(self):
        self.parent_class.blit(self.image.image_surface, (0, 0))


class LevelCard(Surface):
    # продумать реиспользование методов принятие аргументов или работа полностью через self
    # продумать надо ли здесь что-то и как-то с группами мудрить
    FRAME_COLOR = (128, 0, 128)
    MARGIN_COEFF = 0.05

    def __init__(self, image, width, height, x, y):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.image = image
        # подумать апдейтить здесь размер картинки или как-то сразу сюда передавать правильный размер
        self.update_image_size()
        self.create()

    def create(self):
        x = self.calculate_margin_width()
        y = self.calculate_margin_height()
        self.fill(self.FRAME_COLOR)
        self.blit(self.image.image_surface, (x, y))

    def calculate_margin_width(self):
        return self.width * self.MARGIN_COEFF

    def calculate_margin_height(self):
        return self.height * self.MARGIN_COEFF

    def calculate_image_size(self):
        margin_width = self.calculate_margin_width()
        margin_height = self.calculate_margin_height()

        width = self.width - margin_width * 2
        height = self.height - margin_height * 2

        return width, height

    def update_image_size(self):
        image_size = self.calculate_image_size()
        if (self.image.width, self.image.height) != image_size:
            self.image.scale(*image_size)
