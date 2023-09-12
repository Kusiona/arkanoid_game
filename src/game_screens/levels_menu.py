import pygame
from pygame.surface import Surface
from src.common.image import LevelCard
from src.common.base.image import Image
from src.common.base.font import Font
from src.common.buttons import LevelsMenuBackButton, LevelButton


class InterfaceLevelCardsBlock:
    CARDS_COLS = 3
    CARDS_ROWS = 3
    CARDS_PADDING_COEFF = 0.01

    def __init__(self, interface, parent_class, read_existed=False):
        self.parent_class = parent_class
        self.parent_class.main_app_class.extra_event_handlers.append(self.handle_event)
        self.interface = interface
        self.width, self.height = self.parent_class.get_size()
        if read_existed:
            self.place_cards()
        else:
            self.create_levels_cards()

    def place_cards(self):
        # узнать есть ли какой-то draw у сюрфэйсов как у спрайтов
        for card in self.parent_class.main_app_class.levels_cards:
            card.parent_class = self.parent_class
            self.parent_class.main_app_class.extra_event_handlers.append(card.handle_event)
            card.render(card.image.x, card.image.y)

    def get_cards_padding_width(self):
        return self.width * self.CARDS_PADDING_COEFF

    def get_cards_padding_height(self):
        return self.height * self.CARDS_PADDING_COEFF

    def get_card_size(self):
        available_width = self.interface.get_available_width()
        available_height = self.interface.get_available_height()
        cards_padding_width = self.get_cards_padding_width()
        cards_padding_height = self.get_cards_padding_height()

        width = (available_width - cards_padding_width) / self.CARDS_COLS
        height = (available_height - cards_padding_height) / self.CARDS_ROWS

        return width, height

    def create_levels_cards(self):
        # нет учета self.CARDS_ROWS
        # в будущем сделать пролистывание уровней, если их больше чем влезает в указанные столбцы и строки
        cards = []
        x = self.interface.get_cards_block_padding_width()
        y = self.interface.get_cards_block_padding_height()
        card_size = self.get_card_size()
        levels_config = self.parent_class.main_app_class.levels_config
        col_index = 1
        for level_name in levels_config:
            card = LevelCard(levels_config[level_name]['background_image_thumb'], *card_size, x, y)
            level_card_button = LevelButton(
                    self.parent_class, card, level_name
                )
            level_card_button.render(card.x, card.y)
            cards.append(level_card_button)
            x += card_size[0] + self.get_cards_padding_width()

            if col_index % self.CARDS_COLS == 0:
                x = self.interface.get_cards_block_padding_width()
                y += card_size[1] + self.get_cards_padding_height()

            col_index += 1

        self.parent_class.main_app_class.levels_cards = cards

    def handle_event(self, event):
        pass


class LevelMenuInterface:
    # продумать реиспользование методов принятие аргументов или работа полностью через self
    # текст учитывает только высоту, не учитывает ширину

    TITLE_TEXT = 'LEVELS'
    TITLE_FONT_SIZE_COEFF = 0.9
    BUTTONS_FONT_SIZE_COEFF = 0.4
    CARDS_BLOCK_PADDING_COEFF = 0.15

    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.main_app_class = parent_class.main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.width, self.height = self.parent_class.get_size()
        self.cards_block = None
        self.render()

    def render(self):
        self.create_title()
        read_existed_cards = True if hasattr(self.main_app_class, 'levels_cards') else False
        self.create_levels_cards(read_existed_cards)
        self.create_back_button()

    def create_levels_cards(self, read_existed_cards=False):
        self.cards_block = InterfaceLevelCardsBlock(
            self, self.parent_class, read_existed=read_existed_cards
        )

    def get_font_size_by_coeff(self, coeff):
        padding_height = self.get_cards_block_padding_height()
        padding_width = self.get_cards_block_padding_width()
        size = int(padding_width * coeff)
        if padding_height < padding_width:
            size = int(padding_height * coeff)
        return size

    def create_title(self):
        font_size = self.get_font_size_by_coeff(self.TITLE_FONT_SIZE_COEFF)
        font = Font(self.TITLE_TEXT, font_size)
        text_width, text_height = font.surface.get_width(), font.surface.get_height()
        x = (self.width - text_width) / 2
        y = (self.get_cards_block_padding_height() / 2) - (text_height / 2)
        self.parent_class.blit(
            font.shadow_surface,
            (
                font.get_shadow_x(x, font_size),
                font.get_shadow_y(y, font_size),
            )
        )
        self.parent_class.blit(font.surface, (x, y))

    def create_back_button(self):
        text_size = self.get_font_size_by_coeff(self.BUTTONS_FONT_SIZE_COEFF)
        back_button = LevelsMenuBackButton(
            parent_class=self.parent_class,  text_size=text_size
        )
        x = (self.width / 2) - (back_button.width / 2)
        y = self.height - (self.get_cards_block_padding_height() / 2) - (back_button.height / 2)
        back_button.render(x, y)

    def get_cards_block_padding_width(self):
        return self.width * self.CARDS_BLOCK_PADDING_COEFF

    def get_cards_block_padding_height(self):
        return self.height * self.CARDS_BLOCK_PADDING_COEFF

    def get_available_width(self):
        return self.width - self.get_cards_block_padding_width() * 2

    def get_available_height(self):
        return self.height - self.get_cards_block_padding_height() * 2

    def handle_event(self, event):
        if event.type == pygame.WINDOWRESIZED:
            self.width, self.height = event.x, event.y
            self.create_levels_cards()


class LevelsMenu(Surface):
    interface_class = LevelMenuInterface
    # DYNAMIC = False

    def __init__(self, main_app_class):
        super().__init__((main_app_class.WIDTH, main_app_class.HEIGHT))
        self.main_app_class = main_app_class
        self.main_app_class.extra_event_handlers.append(self.handle_event)
        self.render()
        self.interface = self.interface_class(parent_class=self)

    def set_background(self, image):
        self.blit(image, (0, 0))

    def render(self):
        background_exists = hasattr(self.main_app_class, 'background')
        background = self.main_app_class.background if background_exists else None
        filename = 'level_menu_bg.jpg'
        if not background_exists or background and not background.source_class == str(self):
            self.main_app_class.background = Image(
                filename, source_class=str(self),
                width=self.get_width(), height=self.get_height()
            )

        self.set_background(self.main_app_class.background.image_surface)

    def handle_event(self, event):
        if event.type == pygame.WINDOWRESIZED:
            self.main_app_class.background.scale(
                # абсолютно не понятно почему я не могу взять собственные get_width get_height, выяснить
                self.main_app_class.WIDTH, self.main_app_class.HEIGHT
            )
            self.set_background(self.main_app_class.background.image_surface)

    def __str__(self):
        return 'LevelsMenu'
