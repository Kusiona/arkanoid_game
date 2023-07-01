from pygame.rect import Rect


class Button(Rect):
    # todo button_text button_text_shadow непонятно зачем на уровне класса, а не экземпляра
    button_text = ''
    button_text_shadow = ''
    # todo константы капсом
    color = (25, 25, 112)
    shadow_color = (128, 0, 128)

    def __init__(self, screen, text, font, text_size, text_x, text_y, action):
        super().__init__(text_x, text_y, text_size[0], text_size[1])
        self.screen = screen
        # todo одно и тоже значение у двух аттрибутов и оно будет одно и тоже всегда,
        #  надо сделать один аттрибут
        self.text = text
        self.text_shadow = text
        self.font = font
        self.action = action

    def create(self):
        self.button_text = self.font.render(self.text, True, self.color)
        self.button_text_shadow = self.font.render(self.text_shadow, True, self.shadow_color)
