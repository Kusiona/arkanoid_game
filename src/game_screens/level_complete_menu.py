from src.common.base.base_interface import BaseInterface
from src.common.base.base_menu import BaseMenu


class LevelCompleteInterface(BaseInterface):

    def __init__(self, parent_class):
        super().__init__(parent_class)

    def create_buttons(self):
        # to avoid circular imports
        from src.common.buttons import ExitMenuButton

        font_size = self.get_font_size(self.parent_class.config['buttons_font_coeff'])
        exit_menu_button = ExitMenuButton(
            parent_class=self.parent_class,
            text_size=font_size
        )
        x = (self.width / 2) - (exit_menu_button.width / 2)
        y = self.height / 2 + font_size * 2
        exit_menu_button.render(x, y)


class LevelCompleteMenu(BaseMenu):
    CONFIG_KEY = 'level_complete_menu'
    interface_class = LevelCompleteInterface

    def __init__(self, main_app_class):
        super().__init__(main_app_class)
