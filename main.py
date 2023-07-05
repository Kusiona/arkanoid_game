import pygame
import sys
from main_menu import BackgroundImage, MainMenuSurface
from level_menu import BackgroundLevelMenu


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

    def run_game_loop(self):
        background = BackgroundImage(time_interval=0.25, width=self.WIDTH, height=self.HEIGHT)

        while self.game:
            self.WIDTH = self.screen.get_width()
            self.HEIGHT = self.screen.get_height()

            # todo MainMenuSurface и BackgroundLevelMenu должны создаваться один раз
            #  и просто лепиться на каждой итерации цикла. Не надо их создавать на каждой итерации
            if self.screen_number == '1':
                self.current_screen = MainMenuSurface(width=self.WIDTH, height=self.HEIGHT, background=background)
                self.current_screen.collect_main_menu(clock=self.clock, fps=self.FPS)
                self.screen.blit(self.current_screen, (0, 0))

            if self.screen_number == '2':
                self.current_screen = BackgroundLevelMenu(width=self.WIDTH, height=self.HEIGHT)
                self.current_screen.create_background_image()
                self.screen.blit(self.current_screen, (0, 0))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.screen_number = self.current_screen.handle_event(event)
                    # todo вынести в отдельный метод выход из игры, чтобы избежать копипаста
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# todo подумать как все таки иметь на уровне экземпляра один единственный рабочий screen
#  а не в виде какой-то локально переменной в функции
# todo для текста сделать отдельный класс унаследованный от библиотечного текста, внутри которого будет реализовываться смещение
# todo спроектировать грамотный принцип работы главного класса игры с рабочими экранами
# todo спроектировать грамотный принцип работы всех поверхностей и интерактивных элементов на экране с ивентами
if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
