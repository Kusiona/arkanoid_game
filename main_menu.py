import pygame
from buttons import Button
from pygame.surface import Surface


class BaseInterface:
    FONT = 'fonts/InvasionBold.ttf'

    def __init__(self, width, height, main_surface):
        self.main_surface = main_surface
        self.width = width
        self.height = height
        self.main_text = None
        self.text_shadow = None
        self.text_x = None
        self.text_y = None
        self.play_button = None
        self.exit_button = None

    def create_background_image(self, clock, fps, background_image):
        pass

    def create_text(self, text, size, coefficient):
        font = pygame.font.Font(self.FONT, size)
        self.main_text = font.render(text, True, (25, 25, 112))
        self.text_shadow = font.render(text, True, (128, 0, 128))
        text_width, text_height = font.size(text)
        self.text_x = (self.width - text_width) / 2
        self.text_y = ((self.height / 2) - text_height) / coefficient

    def create_buttons(self,  text, size, coefficient):
        font = pygame.font.Font(self.FONT, size)
        text_size = font.size(text)
        self.text_x = (self.width - text_size[0]) / 2
        self.text_y = self.height - (self.height / coefficient)

        button = Button(text_size=text_size, text_x=self.text_x, text_y=self.text_y)
        button.create(screen=self, text=text, font=pygame.font.Font(self.FONT, size), action=text)

        if text == 'PLAY':
            self.play_button = button
        elif text == 'EXIT' or text == 'BACK':
            self.exit_button = button
        self.main_text = button.button_text
        self.text_shadow = button.button_text_shadow

    def build_interface(self, clock, fps, background_image):
        pass


class MainMenuInterface(BaseInterface):

    def __init__(self, width, height, main_surface):
        super().__init__(width=width, height=height, main_surface=main_surface)
        self.surface = main_surface

    def create_background_image(self, clock, fps, background_image):
        seconds = clock.tick(fps) / 300.0
        background_image.update(seconds)
        self.main_surface.blit(background_image.image, (0, 0))

    def build_interface(self, clock, fps, background_image):
        self.create_text(text='ARKANOID', coefficient=2, size=130)

        self.create_background_image(clock=clock, fps=fps, background_image=background_image)

        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 5, self.text_y + 5))

        self.create_buttons(text='PLAY', size=100, coefficient=2)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 4, self.text_y + 4))

        self.create_buttons(text='EXIT', size=100, coefficient=4)
        self.main_surface.blit(self.main_text, (self.text_x, self.text_y))
        self.main_surface.blit(self.text_shadow, (self.text_x + 4, self.text_y + 4))


class MainMenu(Surface):
    interface = MainMenuInterface

    def __init__(self, width, height):
        super().__init__((width, height))
        self.interface = MainMenuInterface(main_surface=self, width=width, height=height)

    def handle_event(self, event):
        if self.interface.play_button.collidepoint(event.pos):
            return '2'
        elif self.interface.exit_button.collidepoint(event.pos):
            self.interface.exit_button.exit()
        return '1'
