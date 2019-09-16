from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from random import choice
import settings

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI),use_aliases=True)
        return user_data['emo']

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика','Сменить аватарку'],
                                        [contact_button,location_button]
                                        ], resize_keyboard=True
                                        )
    return my_keyboard

def wordcount(bot, update, user_data):
    user_text = update.message.text
    try:
        words=len(user_text.split())-1
        if words%10 == 1:
            wd='слово'
        elif words%10 > 1 and words%10 < 5:
            wd='слова'
        elif words%10 >= 0:
            wd='слов'
        text='В тексте всего {} {}.'.format(words,wd)
    except:
        text='Напишите текст и я скажу сколько в нём слов'
    update.message.reply_text(text)


