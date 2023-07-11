import pygame
from pygame.surface import Surface
from pygame.transform import scale
from processing_image import Image
from levels import LevelSurface
from main_menu import BaseInterface


class LevelMenuInterface(BaseInterface):

    def __init__(self, width, height, main_surface):
        super().__init__(width=width, height=height, main_surface=main_surface)
        self.image = Image(width=width, height=height)
        self.level_surface = None

    def create_background_image(self, clock, fps, background_image):
        self.image.create_lvl_menu_bg_img()
        self.image = scale(self.image.image, (self.width, self.height))
        self.main_surface.blit(self.image, (0, 0))

    def build_interface(self, clock, fps, background_image):
        self.create_text(text='LEVELS', coefficient=5, size=70)
        self.create_background_image(clock=clock, fps=fps, background_image=self.image)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 5, self.text_y + 5))

        self.create_buttons(text='BACK', coefficient=7, size=50)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 4, self.text_y + 1))

        self.collect_level_list(clock=clock, fps=fps)

    def collect_level_list(self, clock, fps):
        self.level_surface = LevelSurface(width=self.width, height=self.height, clock=clock, fps=fps)
        self.level_surface.get_level_icon(main_surface=self.main_surface)


class LevelMenu(Surface):
    interface = LevelMenuInterface

    def __init__(self, width, height):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.interface = LevelMenuInterface(width=self.width, height=self.height, main_surface=self)

    def handle_event(self, event):
        if self.interface.exit_button.collidepoint(event.pos):
            return '1'
        # if self.interface.level_surface.level_icon.rect.collidepoint(event.pos):
        return '2'
