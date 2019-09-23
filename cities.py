import csv
from random import choice

#city=''
#user_text = ''
cities_list = []
#чтение из файла в глобальный список
def import_csv(bot, update, user_data):
    with open('city_all.csv', 'r', encoding='cp1251') as f:
        global cities_list
        reader=csv.DictReader(f, delimiter=';')
        for row in reader:
            cities_list.append(row["name"])
    user_text = update.message.text.split(' ')[1].capitalize()
    
#ход пользователя
def user_city(update, user_data):
    global cities_list
    global city
    global user_text
    user_text = update.message.text.split(' ')[1].capitalize()
    try:
        mistake = 3
        if user_text.capitalize()=='Стоп':
            return ('Пока')
        else:
            while user_text not in cities_list and user_text[0].lower()!=city[-1] and mistake!=0:
                print('Нет такого города, не жульничай) У тебя ещё {} попытки!'.format(mistake))
                mistake-=1
                user_text = input('Введи название города на букву {} \n'.format(city[-1].upper())).capitalize()
            else:
                city=user_text
                cities_list.remove(city)
                print('Отлично! Теперь мой город на букву {}...'.format(city[-1].upper()))
                return bot_city()
    except:
        print('Что то ты не то ввёл, пока!')
#ход бота
def bot_city(bot, update, user_data):
    global cities_list
    global city
    global user_text
    user_text=choice(cities_list)
    try:
        if len(city)==0:
            city=choice(cities_list)
            cities_list.remove(city)
            print(city)
            return user_city()
        else:
            while user_text[0].lower()!=city[-1]:
                user_text=choice(cities_list)
            else:
                cities_list.remove(user_text)
                city=user_text
                print(city)
                return user_city()
    except(IndexError):
        print('Города закончились!')
        return False