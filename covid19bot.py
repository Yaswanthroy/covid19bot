import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import requests
import locale
import os
locale.setlocale(locale.LC_ALL, 'en_IN')

BOT_TOKEN = os.environ.get("BOT_API_KEY","")

bot = telegram.Bot(BOT_TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("WORLDWIDE", callback_data='World'),
            InlineKeyboardButton("INDIA", callback_data='india'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose which data u want:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    states=requests.get(os.environ.get("STATE_API_KEY","")).json()
    if query.data == "World":
        world = requests.get(os.environ.get("WORLD_API_KEY","")).json();s=""
        for i in world:
            if i!="updated":
                s+=str(i.upper())+ "  - " +str(locale.format("%d", world[i], grouping=True))+'\n'*2
        bot.send_message(update.effective_user.id, s)
    elif query.data[0] == "+":
        s=""
        for i in states:
            if i["country"]=="India" and i["province"]==query.data[1:]:
                for j in i["stats"]:
                    s+=str(j)+ "  - " +str(locale.format("%d", i["stats"][j], grouping=True)) + "\n"*2
        bot.send_message(update.effective_user.id, s) 
    else:
        india = requests.get(os.environ.get("INDIA_API_KEY","")).json();s=""
        for i in india:
            if i!="updated" and i!="countryInfo":
                out=india[i].upper() if type(india[i])==str else locale.format("%d", india[i], grouping=True)
                s += str(i.upper()) + "  - " + str(out) + "\n"*2
        bot.send_message(update.effective_user.id, s) 
        keyboard = []
        for i in states:
            if i["country"]=="India" and i["province"]!="Unknown":
                keyboard += [
                    [
                        InlineKeyboardButton(i["province"], callback_data="+" + str(i["province"])),
                    ],
                ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(update.effective_user.id, 'INDIA STATES', reply_markup=reply_markup)

    query.answer()


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
