import pygame
from pygame.surface import Surface
from pygame.transform import scale
from buttons import Button
from levels import LevelSurface


# todo понять, как отнаследоваться от уже существующего такого класса с нужными мне изменениями
class LevelMenuInterface(Surface):
    FONT = 'fonts/InvasionBold.ttf'

    def __init__(self, width, height, image, main_surface):
        super().__init__((width, height))
        self.main_surface = main_surface
        self.width = width
        self.height = height
        self.main_text = None
        self.text_shadow = None
        self.text_x = None
        self.text_y = None
        self.image = image
        self.button = None
        self.level_surface = None

    def create_background_image(self):
        self.image = scale(self.image, (self.width, self.height))
        self.main_surface.blit(self.image, (0, 0))

    def create_text(self, text):
        font = pygame.font.Font(self.FONT, 70)
        self.main_text = font.render(text, True, (25, 25, 112))
        self.text_shadow = font.render(text, True, (128, 0, 128))
        text_width, text_height = font.size(text)
        self.text_x = (self.width - text_width) / 2
        self.text_y = ((self.height / 2) - text_height) / 5

    def create_buttons(self, text, coefficient):
        font = pygame.font.Font(self.FONT, 50)
        text_size = font.size(text)
        self.text_x = self.width - ((self.width - text_size[0]) / 4)
        self.text_y = self.height - (self.height / coefficient)

        self.button = Button(text_size=text_size, text_x=self.text_x, text_y=self.text_y)
        self.button.create(screen=self, text=text, font=pygame.font.Font(self.FONT, 50), action=text)
        self.main_text = self.button.button_text
        self.text_shadow = self.button.button_text_shadow

    def collect_level_list(self, clock, fps):
        self.level_surface = LevelSurface(width=self.width, height=self.height, clock=clock, fps=fps)
        self.level_surface.create_level_icon(main_surface=self.main_surface)

    def collect_surface(self, clock, fps):
        self.create_text(text='LEVELS')
        self.create_background_image()
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 5, self.text_y + 5))

        self.create_buttons(text='BACK', coefficient=7)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 4, self.text_y + 1))

        self.collect_level_list(clock=clock, fps=fps)


class LevelMenuSurface(Surface):
    BG_IMAGE = 'images/level_menu.jpg'

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.level_menu = None
        self.image = pygame.image.load(self.BG_IMAGE)

    def collect_menu(self, clock, fps):
        self.level_menu = LevelMenuInterface(width=self.width, height=self.height, image=self.image, main_surface=self)
        self.level_menu.collect_surface(clock=clock, fps=fps)

    def handle_event(self, event):
        if self.level_menu.button.collidepoint(event.pos):
            return '1'
        return '2'
