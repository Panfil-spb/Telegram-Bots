import logging

from hendlers import *
from telegram.ext import Updater, Filters, \
    CommandHandler, Defaults, \
    CallbackQueryHandler, MessageHandler

TOKEN = ""

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    dafults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(token=TOKEN, defaults=dafults)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(btn_hendler))
    dispatcher.add_handler(MessageHandler(Filters.photo, save))
    dispatcher.add_handler(MessageHandler(Filters.text, update_txt))
    updater.start_polling()

    updater.idle()

    pass


if __name__ == '__main__':
    main()
