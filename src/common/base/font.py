from pygame.font import Font


class Font(Font):
    CONFIG_KEY = 'font'
    ANTIALIAS = True

    def __init__(self, main_app_class, text, size):
        self.config = main_app_class.config[self.CONFIG_KEY]
        super().__init__(self.config['font_path'], size)
        self.text = text
        self.size = size
        self.shadow_surface = None
        self.surface = self.render()

    def render(self):
        self.shadow_surface = super().render(self.text, self.ANTIALIAS, self.config['shadow_color'])
        self.surface = super().render(self.text, self.ANTIALIAS, self.config['color'])
        return self.surface

    def get_shadow_x(self, x, font_size) -> None:
        return x + font_size * self.config['shadow_offset_coeff']

    def get_shadow_y(self, y,  font_size) -> None:
        return y + font_size * self.config['shadow_offset_coeff']
