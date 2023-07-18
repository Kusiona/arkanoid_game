import pygame
from buttons import Button
from pygame.surface import Surface
from processing_image import Image
from pygame.time import Clock
from pygame.event import Event


class BaseInterface:
    FONT = 'fonts/InvasionBold.ttf'

    def __init__(self, width: int, height: int, main_surface):
        self.main_surface = main_surface
        self.width = width
        self.height = height
        self.main_text = None
        self.text_shadow = None
        self.text_x = None
        self.text_y = None
        self.lvl_menu_button = None
        self.exit_button = None

    def create_background_image(self, clock, fps, background_image) -> None:
        pass

    def create_text(self, text: str, size: int, coefficient: int) -> None:
        font = pygame.font.Font(self.FONT, size)
        self.main_text = font.render(text, True, (25, 25, 112))
        self.text_shadow = font.render(text, True, (128, 0, 128))
        text_width, text_height = font.size(text)
        self.text_x = (self.width - text_width) / 2
        self.text_y = ((self.height / 2) - text_height) / coefficient

    def create_buttons(self,  text: str, size: int, coefficient: int) -> None:
        font = pygame.font.Font(self.FONT, size)
        text_size = font.size(text)
        self.text_x = (self.width - text_size[0]) / 2
        self.text_y = self.height - (self.height / coefficient)

        button = Button(text_size=text_size, text_x=self.text_x, text_y=self.text_y)
        button.create(screen=self, text=text, font=pygame.font.Font(self.FONT, size), action=text)

        if text == 'CHOOSE LEVEL':
            self.lvl_menu_button = button
        elif text == 'EXIT' or text == 'BACK':
            self.exit_button = button
        self.main_text = button.button_text
        self.text_shadow = button.button_text_shadow

    def build_interface(self, clock: Clock, fps: int, background_image: Image) -> None:
        pass


class MainMenuInterface(BaseInterface):

    def __init__(self, width: int, height: int, main_surface):
        super().__init__(width=width, height=height, main_surface=main_surface)
        self.surface = main_surface

    def create_background_image(self, clock: Clock, fps: int, background_image: Image) -> None:
        seconds = clock.tick(fps) / 300.0
        background_image.update(seconds)
        self.main_surface.blit(background_image.image, (0, 0))

    def build_interface(self, clock: Clock, fps: int, background_image: Image) -> None:
        self.create_text(text='ARKANOID', coefficient=2, size=130)

        self.create_background_image(clock=clock, fps=fps, background_image=background_image)

        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 5, self.text_y + 5))

        self.create_buttons(text='PLAY COMPANY', size=70, coefficient=2)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 3, self.text_y + 3))

        self.create_buttons(text='CHOOSE LEVEL', size=70, coefficient=3)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 3, self.text_y + 3))

        self.create_buttons(text='EXIT', size=70, coefficient=6)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 3, self.text_y + 3))


class MainMenu(Surface):
    interface = MainMenuInterface

    def __init__(self, width: int, height: int):
        super().__init__((width, height))
        self.interface = MainMenuInterface(main_surface=self, width=width, height=height)

    def handle_event(self, event: Event) -> tuple[str, int]:
        if self.interface.lvl_menu_button.collidepoint(event.pos):
            return '2', 0
        elif self.interface.exit_button.collidepoint(event.pos):
            self.interface.exit_button.exit()
        return '1', 0
