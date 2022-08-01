import datetime

import keybords
import sql
from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def get_log(update: Update) -> str:
    """функция генерации лога действия"""
    return f'{datetime.datetime.now().strftime("%m.%d.%Y - %H:%M")} -- {update.effective_user.first_name} {update.effective_user.last_name} -- '


def get_name(update: Update) -> str:
    """функция получения имени пользователя"""
    return f'{update.effective_user.first_name}_{update.effective_user.last_name}'


def menu(update: Update, context: CallbackContext) -> None:
    """ Функция для загрузки меню с сайта """
    if update.callback_query.data == 'menu':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Поджди, меню загружается...')
        context.bot.send_document(chat_id=update.effective_chat.id, document='http://karaoke-duet.ru/menu/duet.pdf')


def help(quary: CallbackQuery) -> None:
    """ Обработка кнопки что бы прислать краткую информацию о главном меню """

    text = "Кнопка 'Бар' - перейти в меню просмотра ттк бара" \
           "\nКнопка 'Кухня' - перейти в меню просмотра ттк кухни" \
           "\nКнопка 'Меню' - бот пришлет меню с сайта" \
           "\nКнопка 'Нет монет' - вы сможете загрузить боту qr-код сервиса или запросить ранее загруженный" \
           "\nКнопка 'Загородный' - вы сможете запросить и изменить стоп листы данного заведения" \
           "\nКнопка 'Белинского' - вы сможете запросить и изменить стоп листы данного заведения"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('<- Назад', callback_data='back_to_main')]])
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def bar(quary: CallbackQuery) -> None:
    """функция кнопки из главного меню бара"""
    text = 'Выберете нужную подгруппу бара'
    reply_markup = keybords.main_bar_keybord
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def kitchen(quary: CallbackQuery) -> None:
    """функция кнопки из главного меню кухни"""

    text = 'Выберете нужную подгруппу кухни'
    reply_markup = keybords.main_kitchen_keybord
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def no_coin(quary: CallbackQuery) -> None:
    """функция кнопки из главного меню нет монет"""
    text = 'Что хотите сделать...'
    reply_markup = keybords.main_no_coin_keyboard
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def back_to_main(quary: CallbackQuery) -> None:
    """функция кнопки возвращающей в главное меню"""
    text = 'Привет, я бот помошник караоке-клуба дуэты.\nЧтобы продолжить выберете то что вам нужно.'
    reply_markup = keybords.main_keybord
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def bar_buttons_func(quary: CallbackQuery) -> None:
    """функция для перехода в подгруппы бара"""
    text = 'Выберете то, что вас интересует'
    reply_markup = keybords.generate_keybord(f'files/bar/{quary.data}.txt', 'photo')
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def kitchen_buttons_func(quary: CallbackQuery) -> None:
    """функция для перехода в подгруппы кухни"""
    text = 'Выберете то, что вас интересует'
    reply_markup = keybords.generate_keybord(f'files/kitchen/{quary.data}.txt', 'exel')
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def send_photo(update: Update, context: CallbackContext) -> None:
    """функция отправки фото"""
    quary = update.callback_query
    mess = get_log(update)
    text = quary.data.split('_')[1]
    try:

        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=open(f'files/photo/{text}.JPG', 'rb'),
                               caption=text)
        print(f'{mess} получил ттк бара {text}')
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ттк нет, но это точно вкусно'
                                      '\nИли просто попробуйте загрузить снова')
        print(f'{mess} не получил ттк бара {text}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=quary.message.text,
                             reply_markup=quary.message.reply_markup)


def send_exel(update: Update, context: CallbackContext) -> None:
    """функция отправки эксель документа"""
    quary = update.callback_query
    mess = get_log(update)
    text = quary.data.split('_')[1]
    try:
        context.bot.send_document(chat_id=update.effective_chat.id,
                                  document=open(f'files/exel/{text}.xlsx', 'rb'),
                                  caption=text)
        print(f'{mess} получил ттк кухни {text}')
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ттк нет, но это точно вкусно'
                                      '\nИли просто попробуйте загрузить снова')
        print(f'{mess} не получил ттк кухни {text}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=quary.message.text,
                             reply_markup=quary.message.reply_markup)


def save_qr(quary: CallbackQuery) -> None:
    """функция перехода в меню сохранения фото"""
    text = 'Загрузите фотографию, и отправьте вместе с сообщением "qr", чтобы сохранить изображение'
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('<- Назад', callback_data='no_coin')]])
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def download_qr(update: Update, context: CallbackContext) -> bool:
    """функция загрузки фото пользователя"""
    quary = update.callback_query
    mess = get_log(update)
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=open(f'files/no_coin/{update.effective_chat.first_name}_'
                                          f'{update.effective_chat.last_name}.jpg', 'rb'))
        print(f'{mess} получил qr "нет монет"')
        return True
    except:
        text = 'Вашего qr еще нет\nЧто хотите сделать...'
        reply_markup = keybords.main_no_coin_keyboard
        quary.edit_message_text(text=text, reply_markup=reply_markup)
        print(f'{mess} не получил qr "нет монет"')


def zavedenie(quary: CallbackQuery) -> None:
    """функция выводы меню заведения"""
    if 'zagorodni' in quary.data:
        text = f'Меню заведения на загородном'
    else:
        text = f'Меню заведения на белинского'
    print(quary.data.split('_')[0])
    reply_markup = keybords.generate_keybord_zavedenie(quary.data.split('_')[1])
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def zavedenie_info(quary: CallbackQuery, name: str) -> None:
    """фуекция вывода меню стоп листов заведения"""
    data = quary.data.split('_')
    file_path = f'files/{data[0]}/{data[1].lower()}.txt'
    sql.update_user_file_path(name, file_path)
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        text = ''.join(line for line in file)

    if text == '':
        text = 'Нужно уточнить стоп у'
        if 'Bar' in data[1]:
            text += ' бармена'
        elif 'Kitchen' in data[1]:
            text += ' повара'
        else:
            text = 'Бармен должен заполнить список табаков'
    reply_markup = keybords.generate_keybord_txt_file(quary.data)
    quary.edit_message_text(text=text, reply_markup=reply_markup)


def update_txt_file(quary: CallbackQuery, callback_data: str) -> None:
    """функция изменения текстового файла стоп листов"""
    text = f"{quary.message.text}\n\nЧтобы изменить список просто отправьте одно сообщение с актуальными данными"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('<- Назад', callback_data=callback_data)]])
    quary.edit_message_text(text=text, reply_markup=reply_markup)
