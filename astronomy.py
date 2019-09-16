from datetime import datetime, date
import ephem

def full_moon(bot,update,user_data):
    now=datetime.now()
    user_text = update.message.text
    d='{}/{}/{}'.format(now.year,now.month,now.day)
    text = 'Следующее полнолуние: {}'.format(ephem.next_full_moon(d))
    update.message.reply_text(text)

def planets_constellation(bot, update, user_data):
    try:
        user_text = update.message.text.split(' ')[1].capitalize()
        planet=getattr(ephem, user_text)
        Planet=planet()
        Planet.compute()
        constellation=ephem.constellation(Planet)
        text='Созвездие {}'.format(constellation)
    except:
        text='Нет такой планеты'
    finally:
        update.message.reply_text(text)