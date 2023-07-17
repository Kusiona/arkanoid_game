import pygame
from processing_image import Image
from main_menu import MainMenu
from level_menu import LevelMenu
from buttons import Button
from levels import LevelSurface

# todo MainMenuSurface и BackgroundLevelMenu должны создаваться один раз
#  и просто лепиться на каждой итерации цикла. Не надо их создавать на каждой итерации

class Arkanoid:
    WIDTH = 800
    HEIGHT = 600
    FPS = 30

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.game = True
        self.screen_number = '1'
        self.current_screen = None
        self.background = Image(time_interval=0.25, width=self.WIDTH, height=self.HEIGHT)
        pygame.display.set_caption('Arcanoid')
        pygame.display.set_icon(pygame.image.load('image_main_icon/image_icon.png'))

    def run_game_loop(self):

        while self.game:
            if self.screen.get_width() > 800 or self.screen.get_height() > 600:
                self.WIDTH = self.screen.get_width()
                self.HEIGHT = self.screen.get_height()
            else:
                self.WIDTH = 800
                self.HEIGHT = 600
            self.update(self.screen_number)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.screen_number = self.current_screen.handle_event(event)
                elif event.type == pygame.QUIT:
                    Button(text_size=(self.WIDTH, self.HEIGHT)).exit()

    def create(self, surface):
        self.current_screen = surface
        self.current_screen.interface.build_interface(clock=self.clock, fps=self.FPS, background_image=self.background)
        self.screen.blit(self.current_screen, (0, 0))

    def update(self, screen_info):
        surface = None
        if screen_info[0] == '1':
            surface = MainMenu(width=self.WIDTH, height=self.HEIGHT)
        if screen_info[0] == '2':
            surface = LevelMenu(width=self.WIDTH, height=self.HEIGHT)
        if screen_info[0] == '3':
            surface = LevelSurface(width=self.WIDTH, height=self.HEIGHT, level_number=screen_info[1])

        self.create(surface=surface)

# todo подумать как все таки иметь на уровне экземпляра один единственный рабочий screen
#  а не в виде какой-то локально переменной в функции
# todo для текста сделать отдельный класс унаследованный от библиотечного текста, внутри которого будет реализовываться смещение
# todo спроектировать грамотный принцип работы главного класса игры с рабочими экранами
# todo спроектировать грамотный принцип работы всех поверхностей и интерактивных элементов на экране с ивентами

if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
