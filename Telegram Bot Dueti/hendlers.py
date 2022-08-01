from btn_hendlers import *
from sql import *


def start(update: Update, context: CallbackContext) -> None:
    """ Функция для старта бота """

    text = 'Привет, я бот помошник караоке-клуба дуэты.\nЧтобы продолжить выберете то, что вам нужно.'
    reply_markup = keybords.main_keybord
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    add_user(get_name(update))


def btn_hendler(update: Update, context: CallbackContext) -> None:
    """ Обработка нажатий на кнопках """

    quary = update.callback_query
    mess = get_log(update)
    if quary.data == 'menu':
        """ Обработка кнопки что бы прислать меню """

        print(f'{mess} запросил меню')
        menu(update, context)
        start(update, context)
    elif quary.data == 'help':
        """ Обработка кнопки что бы прислать краткую информацию о главном меню """

        print(f'{mess} запросил помощь с главным меню')
        help(quary)
    elif quary.data == 'bar':
        """ Обработка перехода в подгруппы бара """

        print(f'{mess} зашел в меню бара')
        bar(quary)
    elif quary.data == 'kitchen':
        """ Обработка перехода в подгруппы кухни """

        print(f'{mess} зашел в меню кухни')
        kitchen(quary)
    elif quary.data == 'no_coin':
        """ Обработка перехода в меню 'Нет монет' """

        print(f'{mess} зашел в нет монет')
        no_coin(quary)
    elif quary.data == 'back_to_main':
        """ Обработка перехода в главное меню """

        print(f'{mess} вернулся в главное меню')
        back_to_main(quary)
    elif quary.data in keybords.bar_buttons:
        """ Обработка перехода в подгруппу бара """

        print(f'{mess} першел в подгруппу бара {quary.data}')
        bar_buttons_func(quary)
    elif quary.data in keybords.kitchen_buttons:
        """ Обработка перехода в подгруппу кухни """

        print(f'{mess} першел в подгруппу кухни {quary.data}')
        kitchen_buttons_func(quary)
    elif 'photo' in quary.data:
        """ Обработка нажатия на кнопку позиции бара и отправка фото с ттк """

        send_photo(update, context)
    elif 'exel' in quary.data:
        """ Обработка нажатия на кнопку позиции кухни и отправка документа с ттк """

        send_exel(update, context)
    elif quary.data == 'save_qr':
        """ Обработка перехода в загрузку """

        print(f'{mess} хочет загрузить "нет монет"')
        update_user(get_name(update), flag_qr=True)
        save_qr(quary)
    elif quary.data == 'download_qr':
        """ Загружаем в чат фотографию 'Нет монет' """

        if download_qr(update, context):
            start(update, context)
    elif 'zavedenie' in quary.data:
        zavedenie(quary)
    elif 'stopbar' in quary.data and 'update' not in quary.data:
        zavedenie_info(quary, get_name(update))
    elif 'stopkitchen' in quary.data and 'update' not in quary.data:
        zavedenie_info(quary, get_name(update))
    elif 'kalik' in quary.data and 'update' not in quary.data:
        zavedenie_info(quary, get_name(update))
    elif 'update' in quary.data:
        data = quary.data.split('_')
        zav = data[0]
        file_update = data[1]
        update_user(get_name(update), flag_txt=True)
        update_txt_file(quary, f'{zav}_{file_update}')


def save(update: Update, context: CallbackContext) -> None:
    """ Функция для отсеивания фотографий в не нужный момент"""

    if get_qr_flag(get_name(update)):
        """ Если мы сейчас находимся в нужном меню """

        """ Если сообщение с фотографией совпадают, то сохраняем фото """

        file = context.bot.getFile(update.message.photo[-1].file_id)
        img = context.bot.get_file(file)
        img.download(f'files/no_coin/{update.message.chat.first_name}_{update.message.chat.last_name}.jpg')
        text = 'Qr-код успешно загружен!\nЧто хотите сделать...'
        reply_markup = keybords.main_no_coin_keyboard
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        update_user(get_name(update), flag_qr=False)
    else:
        """ Удалаяем фото из чата """

        context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)


def update_txt(update: Update, context: CallbackContext) -> None:
    """функция для изменения тектового файла стопов"""
    if get_txt_flag(get_name(update)):
        """ Если мы сейчас находимся в нужном меню """

        text = update.message.text
        file_path = get_file_path(get_name(update))
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(file_path)
        name = f'{file_path.split("/")[1]}_{file_path.split("/")[1]}'
        reply_markup = keybords.generate_keybord_txt_file(name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        update_user(get_name(update), flag_txt=False)
    else:
        """ Удалаяем сообщение из чата """

        context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
