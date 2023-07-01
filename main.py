import pygame
import sys
from start_menu import BackgroundImage, MainMenuSurface
from level_menu import BackgroundLevelMenu


class Arkanoid:
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        # todo фпс надо обьявлять на уровне класса как константу
        self.FPS = 30

    def run_game_loop(self):
        # todo сделать game и background_menu атрибутами класса и обьявить их в __init__
        # todo переимонать background_menu -> main_menu
        game = True
        background_menu = True
        background = BackgroundImage(0.25)
        # todo screen по дефолту None пустая строка была бы уместна, если бы дальше былла бы нужна работа со строкой
        screen = ''

        while game:
            self.WIDTH = self.screen.get_width()
            self.HEIGHT = self.screen.get_height()

            # todo MainMenuSurface и BackgroundLevelMenu должны создаваться один раз
            #  и просто лепиться на каждой итерации цикла. Не надо их создавать на каждой итерации
            if background_menu:
                # todo screen -> current_screen
                screen = MainMenuSurface(width=self.WIDTH, height=self.HEIGHT, background=background)
                screen.collect_main_menu(clock=self.clock, fps=self.FPS)
                self.screen.blit(screen, (0, 0))

            if not background_menu:
                screen = BackgroundLevelMenu(width=self.WIDTH, height=self.HEIGHT)
                # todo create_back_image -> create_background_image or create_bg_image  or create_bg_img
                screen.create_back_image()
                self.screen.blit(screen, (0, 0))

            # todo либо/либо не вместе
            # todo update нужен для обновления переданной части экрана
            pygame.display.update()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # todo listen_events -> handle_event 1! evenT класс ничего не слушает, скорее ты даешь ему что-то в обработку
                    background_menu = screen.listen_events(event)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# todo кнопка play откликается на все события на экране, кнопка exit работает корректно
# todo если выбрали что главное меню это main_menu, то везде надо придерживаться этого немйинга
# todo изменить названия файл start_menu
# todo подумать как все таки иметь на уровне экземпляра один единственный рабочий screen
#  а не в виде какой-то локально переменной в функции
# todo для текста сделать отдельный класс унаследованный от библиотечного текста, внутри которого будет реализовываться смещение
# todo спроектировать грамотный принцип работы главного класса игры с рабочими экранами
# todo спроектировать грамотный принцип работы всех поверхностей и интерактивных элементов на экране с ивентами
# todo директория image содержит более одного изображения, учесть в нейминге
if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
