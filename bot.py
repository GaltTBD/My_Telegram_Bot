from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from glob import glob
from datetime import datetime, date
from random import choice
from emoji import emojize

from telegram import ReplyKeyboardMarkup, KeyboardButton
 
import logging
import settings
import ephem

from utils import *
from handlers import *
from astronomy import *


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY)
    logging.info('БОТ ЗАПУСКАЕТСЯ')

    dp = mybot.dispatcher
        
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True)) # обрабатывает команду start
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("wordcount", wordcount, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planets_constellation, pass_user_data=True))

    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(RegexHandler('^(moon)$', full_moon, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True)) # обрабатывает любые текстовые сообщения
    
    mybot.start_polling()
    mybot.idle()
 
if __name__=="__main__":
    main()