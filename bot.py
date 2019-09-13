from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from glob import glob
from random import choice
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
 
from datetime import datetime, date
import logging
import settings
import ephem

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

contact_button = KeyboardButton('Contact info', request_contact=True)
location_button = KeyboardButton('Location', request_location=True)

my_keyboard = ReplyKeyboardMarkup([['See cat!','moon'],['111','222'],[contact_button, location_button]])
now=datetime.now()
def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Thanks {}'.format(get_contact(user_data)))

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Thanks {}'.format(get_location(user_data)))

def wordcount(bot, update, user_data):
    user_text = update.message.text
    if len(user_text) > 1:
        text='Len: {}'.format(len(user_text.split(' '))-1)
    else:
        text='Input some text and i will tell you how many words in it'    
    update.message.reply_text(text)

def full_moon(bot,update,user_data):
    user_text = update.message.text
    d='{}/{}/{}'.format(now.year,now.month,now.day)
    text = 'Next full MOON: {}'.format(ephem.next_full_moon(d))
    update.message.reply_text(text)

def get_user_emo(user_data):
    smile = emojize(choice(settings.USER_EMOJI),use_aliases=True)
    return smile

def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Hello {}'.format(emo)
    #my_keyboard = ReplyKeyboardMarkup([['/cat']])
    update.message.reply_text(text, reply_markup=my_keyboard)   

def talk_to_me(bot, update, user_data):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def send_cat_picture(bot, update, user_data):
    cat_list = glob("images/cat*.jp*g")
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, "rb"))

def main():
    mybot = Updater(settings.API_KEY)

    dp = mybot.dispatcher
        
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("wordcount", wordcount, pass_user_data=True))

    dp.add_handler(RegexHandler('^(See cat!)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(moon)$', full_moon, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()
 
main()