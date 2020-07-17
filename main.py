from telebot import types
import random
import config
import telebot
import requests
from bs4 import BeautifulSoup as BS

r = requests.get('https://sinoptik.ua/погода-ульяновск')
html = BS(r.content, 'html.parser')
bot = telebot.TeleBot(config.TOKEN)

for el in html.select('#content'):
    temp_now = el.select('.temperature .cur')[0].text
    temp_max = el.select('.temperature .max')[0].text
    text = el.select('.wDescription .description')[0].text

layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                           "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

@bot.message_handler(commands=["start"])
def main(message):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.add(types.KeyboardButton(text="Прогноз погоды ⛅"))
    menu_keyboard.add(types.KeyboardButton(text="Рандом 🎲"))
    menu_keyboard.add(types.KeyboardButton(text="Перевод раскладки"))
    menu_keyboard.add(types.KeyboardButton(text="Помощь"))
    menu_keyboard.add(types.KeyboardButton(text="Отмена"))
    bot.send_message(message.chat.id,"Используйте кнопки ниже для взаимодействия с ботом!", reply_markup=menu_keyboard)

@bot.message_handler(commands=["help"])
def welcome(message):
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,"Приветствую тебя, <strong>{0.first_name}</strong>! \n\nМеня зовут <b>danila73bot</b>\n\nИ вот что я могу: \n•Покзать температуру в Ульяновске ⛅ \n•Выбрать рандомное число 🎲 \n•Перевести текст с английской на русскую раскладку \n Для работы используйте меню".format(message.from_user), parse_mode='html')
    bot.send_message(message.chat.id,"Введите /start чтобы начать работу 😎")


@bot.message_handler(content_types = ['text'])
def keyboard_answer(message):
    if message.text == 'Прогноз погоды ⛅':
        bot.send_message(message.chat.id,
                               "Прогноз погоды в городе Ульяновск на данный момент и максимальная:\n" + 'Сейчас ' + temp_now + ', ' + temp_max + '\n' + text)
    elif message.text == 'Рандом 🎲':
        bot.send_message(message.chat.id, str(random.randint(1, 1000)))
    elif message.text == 'Помощь':
        welcome(message)
    elif message.text == 'Отмена':
        action_cancel(message)
    elif message.text == 'Перевод раскладки':
        bot.send_message(message.chat.id, 'Отлично! Введи text')
        bot.register_next_step_handler(message, text_translate)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю \nНе забывайте про меню с коммандами /start")

@bot.message_handler(lambda message: message.text == "Отмена")
def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,"Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)


def text_translate(message):
    bot.send_message(message.chat.id, message.text.translate(layout))


if __name__ == '__main__':
    bot.polling(none_stop=True)