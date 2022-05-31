import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import serial

dev = serial.Serial("/dev/cu.usbserial-110", baudrate=19200)

TOKEN = "5330205048:AAEZkUKglQb8SAx4pnEzsBo75ovQ9f6sAso"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

list_drawings = [
    "circle",
    "square",
    "triangle",
    "star",
    "heart",
    "spare",
    "spare",
    "spare",
    "spare",
    "spare",
    "spare",
    "spare",
    "spare",
    "spare"
]


def generate_keyboard_drawings():
    keyboard_drawings = list()
    c = 0
    temp = list()
    for drawing in list_drawings:
        temp.append(InlineKeyboardButton(text=drawing, callback_data=drawing))
        if c >= 3:
            keyboard_drawings.append(temp)
            temp = list()
            c = 0
        c += 1
    keyboard_drawings.append(temp)
    return keyboard_drawings


def generate_keyboard_drawings_better():
    buttons = [InlineKeyboardButton(text=drawing, callback_data=drawing) for drawing in list_drawings]
    fixedarr = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]
    return fixedarr


def start(update, context):
    text = "Hello, I'm a bot!\nMy purpose is to help remote control your sand table to get any design you like!\nType " \
           "in /drawings to continue "
    update.message.reply_text(text)


def help(update, context):
    text = "Type /start to see the start message and start controlling your sand table remotely!\nYou can type in " \
           "/drawings at any time to get the list of drawings and select one! "
    update.message.reply_text(text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def drawings(update, context):
    """"""
    text="Select one geometric form and wait for the magic to happen!"
    update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(generate_keyboard_drawings_better()))


def handle_button_click(update, context):
    """Parses the CallbackQuery."""
    query = update.callback_query
    query.answer(text="Drawing a " + query.data, show_alert=False)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    generate_keyboard_drawings_better()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("drawings", drawings))
    dp.add_handler(CallbackQueryHandler(handle_button_click))

    dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
