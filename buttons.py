from pygame.rect import Rect


class Button(Rect):
    COLOR = (25, 25, 112)
    SHADOW_COLOR = (128, 0, 128)

    def __init__(self, screen, text, font, text_size, text_x, text_y, action):
        super().__init__(text_x, text_y, text_size[0], text_size[1])
        self.screen = screen
        self.button_text = None
        self.button_text_shadow = None
        self.text = text
        self.font = font
        self.action = action
        self.create()

    def create(self):
        self.button_text = self.font.render(self.text, True, self.COLOR)
        self.button_text_shadow = self.font.render(self.text, True, self.SHADOW_COLOR)
