import pygame
from processing_image import Image
from main_menu import MainMenu
from level_menu import LevelMenu
from buttons import Button
from levels import LevelSurface

# todo MainMenuSurface и BackgroundLevelMenu должны создаваться один раз
#  и просто лепиться на каждой итерации цикла. Не надо их создавать на каждой итерации


class Arkanoid:
    WIDTH = 700
    HEIGHT = 800
    FPS = 30

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.game = True
        self.screen_info = ('1', None)
        self.current_screen = None
        self.background = Image(time_interval=0.25, width=self.WIDTH, height=self.HEIGHT)
        pygame.display.set_caption('Arcanoid')
        pygame.display.set_icon(pygame.image.load('image_main_icon/image_icon.png'))

        # platform movement
        self.platform_offset = 0
        self.platform_move_left = False
        self.platform_move_right = False

        # movement ball
        self.ball_movement = False

    def run_game_loop(self) -> None:
        while self.game:
            event = None
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.screen_info = self.current_screen.handle_event(event)
                elif event.type == pygame.KEYDOWN and self.screen_info[0] == '3':

                    if event.key == pygame.K_LEFT:
                        self.platform_move_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.platform_move_right = True

                elif event.type == pygame.KEYUP and self.screen_info[0] == '3':

                    if event.key == pygame.K_LEFT:
                        self.platform_move_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.platform_move_right = False
                    elif event.key == pygame.K_SPACE:
                        self.ball_movement = True

                elif event.type == pygame.QUIT:
                    Button(text_size=(self.WIDTH, self.HEIGHT)).exit()

            if self.platform_move_left:
                self.screen_info = self.current_screen.handle_event(event)
            elif self.platform_move_right:
                self.screen_info = self.current_screen.handle_event(event)

            self.WIDTH = self.screen.get_width()
            self.HEIGHT = self.screen.get_height()

            self.update(self.screen_info)

            pygame.display.update()

    def create(self) -> None:
        self.current_screen.interface.build_interface(
            clock=self.clock, fps=self.FPS,
            background_image=self.background
        )
        self.screen.blit(self.current_screen, (0, 0))

    def update(self, screen_info) -> None:
        if screen_info[0] == '1':
            self.current_screen = MainMenu(width=self.WIDTH, height=self.HEIGHT)
        if screen_info[0] == '2':
            self.current_screen = LevelMenu(width=self.WIDTH, height=self.HEIGHT)
        if screen_info[0] == '3':
            self.current_screen = LevelSurface(
                width=self.WIDTH, height=self.HEIGHT,
                level_number=screen_info[1], main_app_class=self
            )

        self.create()

# todo подумать как все таки иметь на уровне экземпляра один единственный рабочий screen
#  а не в виде какой-то локально переменной в функции
# todo для текста сделать отдельный класс унаследованный от библиотечного текста, внутри которого будет реализовываться смещение
# todo спроектировать грамотный принцип работы главного класса игры с рабочими экранами
# todo спроектировать грамотный принцип работы всех поверхностей и интерактивных элементов на экране с ивентами

if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
