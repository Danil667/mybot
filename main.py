#!venv/bin/python
import logging
import config
import requests
import random
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as BS
logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

r = requests.get('https://sinoptik.ua/погода-ульяновск/')
html = BS(r.content, 'html.parser')
for el in html.select('#content'):
    temp_now = el.select('.temperature .cur')[0].text
    temp_max = el.select('.temperature .max')[0].text
    text = el.select('.wDescription .description')[0].text

layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                           "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
# /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.add(types.KeyboardButton(text="Прогноз погоды ⛅"))
    menu_keyboard.add(types.KeyboardButton(text="Рандом 🎲"))
    menu_keyboard.add(types.KeyboardButton(text="Перевод раскладки"))
    menu_keyboard.add(types.KeyboardButton(text="Помощь"))
    menu_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer("Используйте кнопки ниже для взаимодействия с ботом!", reply_markup=menu_keyboard)

#help
@dp.message_handler(commands=["help"])
async def welcome(message):
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Приветствую тебя, <strong>{0.first_name}</strong>! \n\nМеня зовут <b>danila73bot</b>\n\nИ вот что я могу: \n•Покзать температуру в Ульяновске ⛅ \n•Выбрать рандомное число 🎲 \n•Перевести текст с английской на русскую раскладку \n Для работы используйте меню".format(message.from_user), parse_mode='html')
    await message.answer("Введите /start чтобы начать работу 😎")

#“Отмена”
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)

@dp.message_handler(content_types=['text'])
async def keyboard_answer(message: types.message):
    if message.chat.type == 'private':
        if message.text == 'Прогноз погоды ⛅':
            await bot.send_message(message.chat.id, "Прогноз погоды в городе Ульяновск на данный момент и максимальная:\n" + 'Сейчас ' + temp_now + ', ' + temp_max + '\n' + text)
        elif message.text == 'Рандом 🎲':
            await bot.send_message(message.chat.id, str(random.randint(1, 1000)))
        elif message.text == 'Помощь':
            await welcome(message)
        elif message.text == 'Перевод раскладки':
            await bot.send_message(message.chat.id, "Введите текст")
        else:
            await bot.send_message(message.chat.id, message.text.translate(layout))
            await bot.send_message(message.chat.id, "Не забывайте про меню с другими коммандами")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)