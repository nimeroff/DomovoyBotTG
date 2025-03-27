from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_key(width: int,*args: str, **kwargs: str):
    #ИНициализация билдеров для клавиатуры
    menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    #Инициализируем список кнопок
    buttons: list[KeyboardButton]=[]

    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))


    if kwargs:
        for key, val in kwargs.items():
            buttons.append(KeyboardButton(text=val))

    menu.row(*buttons,width=width)
    return menu.as_markup(resize_keyboard=True)


def create_inline_key(width: int,*args: str, **kwargs: str):
    #ИНициализация билдеров для клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    #Инициализируем список кнопок
    buttons: list[InlineKeyboardButton]=[]

    #if args:
    #    for button in args:
    #        buttons.append(InlineKeyboardButton(text=LEXICON_INLINE[button] if button in LEXICON_INLINE else button, callback_data=button))


    if kwargs:
        for key, button in kwargs.items():
            buttons.append(InlineKeyboardButton(text=button, callback_data=key))

    kb_builder.row(*buttons,width=width)
    #return menu.as_markup()


    return kb_builder.as_markup()

def create_inline_key_with_url (width: int, **kwargs: str):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Инициализируем список кнопок
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for key, button in kwargs.items():
            buttons.append(InlineKeyboardButton(text=button, url=key))

    kb_builder.row(*buttons, width=width)
    # return menu.as_markup()

    return kb_builder.as_markup()

