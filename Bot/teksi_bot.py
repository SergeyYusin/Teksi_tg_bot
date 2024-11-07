import webbrowser
from telebot import types
import telebot
import sqlite3
# from telebot.async_telebot import AsyncTeleBot
import asyncio
from smtp import send_ya_mail

token = '7258036631:AAEAhjSRD2LT1njgZlFcxY-t_-9OnrvEncg'

bot = telebot.TeleBot(token)
user_info = {}


@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open(url='https://www.pk-teksi.ru/')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вас приветствует "Бот" ООО ПК ТЭКСИ')
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.pk-teksi.ru/')
    markup.add(btn_1)
    btn_2 = types.InlineKeyboardButton('Требуется поверка', callback_data='poverka')
    btn_3 = types.InlineKeyboardButton('Требуется замена', callback_data='zamena')
    markup.add(btn_2, btn_3)
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name} {message.from_user.last_name}, Чем вам помочь?'.format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def poverka(callback):
    mar = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Перейти на сайт', url='https://www.pk-teksi.ru/uslugi/')
    item_1 = types.InlineKeyboardButton('Оформить заявку', callback_data='zayavka')
    mar.add(item, item_1)
    if callback.text == 'Требуется поверка':
        bot.send_message(callback.chat.id, f'<u>Поверка счетчиков воды</u> - от 900 ₽ за 1 шт\n Также '
                                           f'предоставляются скидки на коллективные заявки. Подробности можно узнать '
                                           f'по телефону (+74997494804 или +74997494796).\n <b>Подробнее '
                                           f'на сайте!</b>', parse_mode='html'.format(callback.from_user),
                         reply_markup=mar)
    elif callback.text == 'Требуется замена':
        zamena(callback)
        # bot.send_message(callback.chat.id, f'<u>Стоимость замены счетчика с нашим прибором</u> от 3750₽❗️\n'
        #                                    f'<u>Стоимость замены счетчика с ВАШИМ прибором</u> от2500₽❗',
        #                  parse_mode='html'.format(callback.from_user), reply_markup=mar)

    elif callback.text == 'Перейти на сайт':
        bot.send_message(callback.chat.id, 'https://www.pk-teksi.ru/')


def zamena(callback):
    mar = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Перейти на сайт', url='https://www.pk-teksi.ru/uslugi/')
    item_1 = types.InlineKeyboardButton('Оформить заявку', callback_data='zayavka_zamena')
    mar.add(item, item_1)
    bot.send_message(callback.chat.id, f'<u>Стоимость замены счетчика с нашим прибором</u> от 3750₽❗️\n'
                                       f'<u>Стоимость замены счетчика с ВАШИМ прибором</u> от2500₽❗',
                     parse_mode='html'.format(callback.from_user), reply_markup=mar)


@bot.callback_query_handler(func=lambda message: True)
def main(message):
    global user_info
    if message.data == 'zayavka':
        poverka1('счетчика воды')
        msg = bot.send_message(message.from_user.id, 'Укажите адрес в формате: \n улица, дом, корпус (если имеется), '
                                                     'квартира, подъезд и этаж, а также номер домофона.')
        bot.register_next_step_handler(msg, fio_step)
        bot.register_next_step_handler(msg, address, user_info)
    if message.data == 'zayavka_zamena':
        zamena1('счетчика воды')
        msg = bot.send_message(message.from_user.id, 'Укажите адрес в формате: \n улица, дом, корпус (если имеется), '
                                                     'квартира, подъезд и этаж, а также номер домофона.')
        bot.register_next_step_handler(msg, fio_step)
        bot.register_next_step_handler(msg, address, user_info)
    elif message.data == 'yes':
        msg = bot.send_message(message.from_user.id, 'Укажите, пожалуйста, ваш номер телефона.')
        bot.register_next_step_handler(msg, phone_step)
        bot.register_next_step_handler(msg, phone, user_info)
    elif message.data == 'no':
        msg = bot.send_message(message.from_user.id, 'Укажите адрес в формате: \n улица, дом, корпус (если имеется), '
                                                     'квартира, подъезд и этаж, а также номер домофона.')
        bot.register_next_step_handler(msg, fio_step)
        bot.register_next_step_handler(msg, address, user_info)
    elif message.data == 'cancel':
        bot.send_message(message.from_user.id, 'Заявка отменена')
    elif message.data == '1yes':
        bot.send_message(message.from_user.id, 'Заявка отправлена, мы вам перезвоним.')
        send_ya_mail(*user_info)
    elif message.data == '1no':
        msg = bot.send_message(message.from_user.id, 'Укажите, пожалуйста, ваш номер телефона.')
        bot.register_next_step_handler(msg, phone_step)
        bot.register_next_step_handler(msg, phone, user_info)
    elif message.data == '1cancel':
        bot.send_message(message.from_user.id, 'Заявка отменена')


def phone_step(message):
    msg = message.text
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='1yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='1no')
    keyboard.add(key_no)
    key_cancel = types.InlineKeyboardButton(text='Отмена заявки', callback_data='1cancel')
    keyboard.add(key_cancel)  # добавляем кнопку в клавиатуру
    question = 'Ваш телефон: ' + str(msg) + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def fio_step(message):
    msg = str(message.text)
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    key_cancel = types.InlineKeyboardButton(text='Отмена заявки', callback_data='cancel')
    keyboard.add(key_cancel)  # добавляем кнопку в клавиатуру
    question = 'Ваш адрес: ' + str(msg) + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def zamena1(massage):
    global user_info
    user_info = 'Замена', massage


def poverka1(massage):
    global user_info
    user_info = 'Поверка', massage

def address(message, user):
    global user_info
    user_info += 'Адрес', message.text


def phone(message, user):
    global user_info
    user_info += 'Телефон', message.text
    return user_info

bot.polling(none_stop=True)

# pip install pyTelegramBotAPI
