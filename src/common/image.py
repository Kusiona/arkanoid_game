from src.common.base.image import Image, scale
from pygame import Surface


class Animation:
    CONFIG_KEY = 'animation'

    def __init__(self, directory, parent_class):
        self.parent_class = parent_class
        self.source_class = str(parent_class)
        self.config = self.parent_class.main_app_class.config[self.CONFIG_KEY]
        self.clock = self.parent_class.main_app_class.clock
        self.fps = self.parent_class.main_app_class.fps
        self.directory = directory
        self.images = self.read_images()
        self.image = self.images[0]
        self.index = 1
        self.timer = 0

    def read_image(self, filename, width, height) -> Image:
        return Image(self.parent_class.main_app_class, filename, width=width, height=height)

    def read_images(self) -> list:
        images = []
        for idx in range(0, 164):
            images.append(self.read_image(
                f'{self.directory}/{idx}.{self.config["frames_file_format"]}',
                *self.parent_class.get_size()
            ))

        return images

    def update(self, parent_class) -> None:
        self.parent_class = parent_class
        seconds = self.clock.tick(self.fps) / self.config["animation_delay"]
        self.timer += seconds

        if self.index == len(self.images):
            self.index = 0

        if self.timer >= self.config["time_interval"]:
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

    def render_frame(self) -> None:
        self.parent_class.blit(self.image.image_surface, (0, 0))


class LevelCard(Surface):
    CONFIG_KEY = 'level_card'

    def __init__(self, main_app_class, image, width, height, x, y):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.image = image
        self.config = main_app_class.config[self.CONFIG_KEY]
        self.update_image_size()
        self.create()

    def create(self) -> None:
        x = self.calculate_margin_width()
        y = self.calculate_margin_height()
        self.fill(tuple(self.config['frame_color']))
        self.blit(self.image.image_surface, (x, y))

    def calculate_margin_width(self) -> None:
        return self.width * self.config['margin_coeff']

    def calculate_margin_height(self) -> None:
        return self.height * self.config['margin_coeff']

    def calculate_image_size(self) -> tuple:
        margin_width = self.calculate_margin_width()
        margin_height = self.calculate_margin_height()

        width = self.width - margin_width * 2
        height = self.height - margin_height * 2

        return width, height

    def update_image_size(self) -> None:
        image_size = self.calculate_image_size()
        if (self.image.width, self.image.height) != image_size:
            self.image.scale(*image_size)
