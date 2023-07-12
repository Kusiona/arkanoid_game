from pygame.surface import Surface
from pygame.transform import scale
from pygame import image
from main_menu import BaseInterface
from pygame.sprite import Group
from processing_image import Image, LevelIcon


class LevelMenuInterface(BaseInterface):

    def __init__(self, width, height, main_surface):
        super().__init__(width=width, height=height, main_surface=main_surface)
        self.image = Image(width=width, height=height)
        self.index = 0
        self.bg_image = None
        self.level_surface = None
        self.icon_group = Group()
        self.level_bg_images = [image.load(f'images/images_level/{i}.jpg') for i in range(1, 10)]

    def create_background_image(self, clock, fps, background_image):
        self.image.create_lvl_menu_bg_img()
        self.image = scale(self.image.image, (self.width, self.height))
        self.main_surface.blit(self.image, (0, 0))

    def build_interface(self, clock, fps, background_image):
        self.create_text(text='LEVELS', coefficient=14, size=70)
        self.create_background_image(clock=clock, fps=fps, background_image=self.image)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 5, self.text_y + 5))

        self.create_buttons(text='BACK', coefficient=9, size=50)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 4, self.text_y + 1))

        self.collect_level_list()

    def collect_level_list(self):
        if not self.icon_group:
            for icon in self.level_bg_images:
                self.icon_group.add(LevelIcon(width=self.width, height=self.height, index=self.index, icon=icon))
                self.index += 1
        self.icon_group.update()
        self.icon_group.draw(self.main_surface)


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
        # todo к каждой иконке привязать rect для прослушки событий, флаги?
        # if self.interface.image.rect.collidepoint(event.pos):
        #     print('тыкнул по иконке')
        return '2'
