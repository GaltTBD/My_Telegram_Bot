from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, ConversationHandler, Filters
from telegram.ext import messagequeue as mq

from db import get_or_create_user, get_user_emo

import logging
import settings

from utils import get_keyboard, get_user_emo, wordcount
from handlers import * #get_contact, get_location, greet_user, talk_to_me, send_cat_picture, change_avatar, check_user_photo, anketa_start, anketa_get_name
from astronomy import full_moon, planets_constellation
#from cities import import_csv


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def my_test(bot, job):
    bot.sendMessage(chat_id=441316564, text='Lovely Spam!')
    job.interval += 5
    if job.interval > 15:
        bot.sendMessage(chat_id=441316564, text='Bye!!')
        job.schedule_removal()
        
subscribers = set()

def main():
    mybot = Updater(settings.API_KEY)
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default = True

    logging.info('БОТ ЗАПУСКАЕТСЯ')

    dp = mybot.dispatcher

    mybot.job_queue.run_repeating(send_updates, 5)

    anketa = ConversationHandler(
        entry_points = [RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],#с чего стартует
        states = {
            "name": [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
            "rating": [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],
            "comment": [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
                        CommandHandler('skip', anketa_skip_comment, pass_user_data=True)]
        },
        fallbacks = [MessageHandler(Filters.text, dontknow, pass_user_data=True)]
    )

    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True)) # обрабатывает команду start
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("wordcount", wordcount, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planets_constellation, pass_user_data=True))
#    dp.add_handler(CommandHandler("cities", import_csv, pass_user_data=True))
    
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(RegexHandler('^(moon)$', full_moon, pass_user_data=True))
    
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True)) # обрабатывает любые текстовые сообщения
    
    mybot.start_polling()
    mybot.idle()
 
if __name__=="__main__":
    main()
