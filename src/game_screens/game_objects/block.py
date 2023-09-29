from pygame.sprite import Sprite
from src.common.base.image import Image


class Block(Sprite):
    INNER_INDENT_COEFF = 0.01
    OUTER_INDENT_COEFF = 0.04

    def __init__(self, parent_class, block,
                 coord_block_map, len_line, len_column,
                 parent_class_width, parent_class_height):
        super().__init__()
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.parent_class_width = parent_class_width
        self.parent_class_height = parent_class_height
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)

        self.block = block
        self.stoutness = self.block['stoutness']
        self.map_x, self.map_y = coord_block_map
        self.len_line = len_line
        self.len_column = len_column
        self.width = self.get_width()
        self.height = self.get_height()

        self.image = Image(self.block['image_path'], self, self.width, self.height).image_surface
        self.x, self.y = self.get_coordinates()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def get_coordinates(self):
        x = self.get_outer_indent_x() + (self.get_inner_indent_x() * self.map_x) + (self.width * self.map_x)
        y = self.get_outer_indent_y() + (self.get_inner_indent_y() * self.map_y) + (self.height * self.map_y)
        return x, y

    def get_outer_indent_x(self):
        return self.parent_class_width * self.OUTER_INDENT_COEFF

    def get_outer_indent_y(self):
        return self.parent_class_height * self.OUTER_INDENT_COEFF

    def get_inner_indent_x(self):
        return self.parent_class_width * self.INNER_INDENT_COEFF

    def get_inner_indent_y(self):
        return self.parent_class_height * self.INNER_INDENT_COEFF

    def get_available_width(self):
        available_width = self.parent_class_width - (
                self.get_outer_indent_x() * 2) - (self.get_inner_indent_x() * (self.len_line - 1))
        if available_width < 0:
            available_width = 0
        return available_width

    def get_available_height(self):
        available_height = (self.parent_class_height / 2) - (
                self.get_outer_indent_y() * 2) - (self.get_inner_indent_y() * (self.len_column - 1))
        if available_height < 0:
            available_height = 0
        return available_height

    def get_width(self):
        if self.get_available_width():
            return self.get_available_width() / self.len_line
        else:
            return 0

    def get_height(self):
        return self.get_available_height() / self.len_column

    def update(self):
        self.parent_class.blit(self.image, (self.x, self.y))

    def handle_collision(self):
        self.stoutness -= 1
        self.parent_class.config['block_map'][self.map_y][self.map_x] = self.stoutness
        if not self.stoutness:
            self.kill()
        else:
            self.image = Image(
                f'level_elements/{self.stoutness}_stoutness_block.jpg',
                self, self.width,
                self.height
            ).image_surface

    def handle_event(self, event):
        pass
