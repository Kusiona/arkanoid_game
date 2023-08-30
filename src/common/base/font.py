from pygame.font import Font


class Font(Font):
    FONT_PATH = 'static/fonts/InvasionBold.ttf'
    COLOR = (128, 0, 128)
    SHADOW_COLOR = (25, 25, 112)
    SHADOW_OFFSET_COEFF = 0.04
    ANTIALIAS = True

    def __init__(self, text, size):
        super().__init__(self.FONT_PATH, size)
        self.text = text
        self.size = size
        self.shadow_surface = None
        self.surface = self.render()

    def render(self):
        self.shadow_surface = super().render(self.text, self.ANTIALIAS, self.SHADOW_COLOR)
        self.surface = super().render(self.text, self.ANTIALIAS, self.COLOR)
        return self.surface

    def get_shadow_x(self, x, font_size):
        return x + font_size * self.SHADOW_OFFSET_COEFF

    def get_shadow_y(self, y,  font_size):
        return y + font_size * self.SHADOW_OFFSET_COEFF
