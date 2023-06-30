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
        self.FPS = 30

    def run_game_loop(self):
        game = True
        background_menu = True
        background = BackgroundImage(0.25)
        screen = ''

        while game:
            self.WIDTH = self.screen.get_width()
            self.HEIGHT = self.screen.get_height()

            if background_menu:
                screen = MainMenuSurface(width=self.WIDTH, height=self.HEIGHT, background=background)
                screen.collect_main_menu(clock=self.clock, fps=self.FPS)
                self.screen.blit(screen, (0, 0))

            if not background_menu:
                screen = BackgroundLevelMenu(width=self.WIDTH, height=self.HEIGHT)
                screen.create_back_image()
                self.screen.blit(screen, (0, 0))

            pygame.display.update()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    background_menu = screen.listen_events(event)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# todo кнопка play откликается на все события на экране, кнопка exit работает корректно
if __name__ == '__main__':
    pygame.init()
    Arkanoid().run_game_loop()
