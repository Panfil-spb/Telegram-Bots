from typing import List, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

""" Названия call_back в главных меню бара и кухни """
bar_buttons = ['kokts', 'avtor_kokts', 'shots', 'sets_shots', 'summer_alko', 'summer_no_alko']
kitchen_buttons = ['brusks', 'garn', 'hots', 'salats', 'sets', 'soup', 'sweet', 'zakus']

main_keybord = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Кухня', callback_data='kitchen'),
            InlineKeyboardButton('Бар', callback_data='bar'),
            InlineKeyboardButton('Меню', callback_data='menu'),
        ],
        [
            InlineKeyboardButton('Загородный', callback_data='zavedenie_zagorodni'),
            InlineKeyboardButton('Белинского', callback_data='zavedenie_belinskogo'),
        ],
        [InlineKeyboardButton('Нет монет', callback_data='no_coin')],
        [InlineKeyboardButton('Помощь', callback_data='help')]
    ]
)

main_bar_keybord = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Коктейли', callback_data='kokts'),
            InlineKeyboardButton('Авторские коктейли', callback_data='avtor_kokts'),
        ],
        [
            InlineKeyboardButton('Шоты', callback_data='shots'),
            InlineKeyboardButton('Сеты шотов', callback_data='sets_shots'),
        ],
        [
            InlineKeyboardButton('Лето Алкогольные', callback_data='summer_alko'),
            InlineKeyboardButton('Лето Безалкогольные', callback_data='summer_no_alko'),
        ],
        [InlineKeyboardButton('<- Назад', callback_data='back_to_main')]

    ]
)

main_kitchen_keybord = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Сеты', callback_data='sets'),
            InlineKeyboardButton('Брускеты', callback_data='brusks'),
            InlineKeyboardButton('Закуски', callback_data='zakus'),
        ],
        [
            InlineKeyboardButton('Горячие блюда', callback_data='hots'),
            InlineKeyboardButton('Супы', callback_data='soup'),
            InlineKeyboardButton('Салаты', callback_data='salats'),
        ],
        [
            InlineKeyboardButton('Десерты', callback_data='sweet'),
            InlineKeyboardButton('Гарниры', callback_data='garn'),
        ],
        [InlineKeyboardButton('<- Назад', callback_data='back_to_main')]
    ]
)

main_no_coin_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Получить QR-код', callback_data='download_qr'),
            InlineKeyboardButton('Сохранить QR-код', callback_data='save_qr')
        ],
        [InlineKeyboardButton('<- Назад', callback_data='back_to_main')]
    ]
)


def build_menu(
        buttons: List[InlineKeyboardButton],
        n_cols: int,
        header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None,
        footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None
) -> List[List[InlineKeyboardButton]]:
    """функция для создания кнопок из списков """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu


def generate_keybord(filename: str, type: str) -> InlineKeyboardMarkup:
    """функция для клавиатуры из записей из файла"""
    buttons = None
    with open(filename, 'r', encoding='utf-8') as file:
        buttons = [InlineKeyboardButton(text=line, callback_data=f'{type}_{line.strip()}') for line in file]
    keybord = build_menu(buttons, 3,
                         footer_buttons=InlineKeyboardButton(text='<- Назад', callback_data=filename.split('/')[1]))
    return InlineKeyboardMarkup(keybord)


def generate_keybord_zavedenie(name: str) -> InlineKeyboardMarkup:
    """функция генерации меню заведения"""
    keybord = [
        [
            InlineKeyboardButton('Стоп бар', callback_data=f'{name}_stopbar'),
            InlineKeyboardButton('Стоп кухня', callback_data=f'{name}_stopkitchen'),
            InlineKeyboardButton('Табаки', callback_data=f'{name}_kalik')
        ],
        [InlineKeyboardButton('<- Назад', callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keybord)


def generate_keybord_txt_file(name: str) -> InlineKeyboardMarkup:
    """функция генерации меню тектового файла"""
    keybord = [
        [
            InlineKeyboardButton('Изменить', callback_data=f'{name}_update'),
        ],
        [InlineKeyboardButton('<- Назад', callback_data=f'zavedenie_{name}')]
    ]
    return InlineKeyboardMarkup(keybord)
