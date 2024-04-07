from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import *
import requests
TOKEN = '6480859175:AAH-8PcaiPB6S2eRWvYBqrN6eCVdbByfQs4'


bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Salom ! Botni ishlatish uchun\n"
                     "Tugmani bosing 🛎",
                     reply_markup=generate_button())

@bot.message_handler(regexp='Ob-xavo')
def ask_city(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Shaxar nomini kiriting",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, answer_to_user)


def answer_to_user(message: Message):
    chat_id = message.chat.id
    text = message.text
    bot.send_message(chat_id, f"Siz kiritgan shaxar: {text}")


    KEY = '6418b539e0697f54de8a3df65ebe9444'
    params = {
        'appid': KEY,
        'units': 'metric',
        'lang': 'en',
        'q': text
    }
    data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?', params=params).json()
    try:
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        sun = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        answer = f'{text} da xozir {description}\nTemperatura: {temp}\nShamol tezligi: {wind_speed}\n' \
             f'Quyosh chiqishi: {sun}\nQuyosh botishi: {sunset}'
        bot.send_message(chat_id, answer)
        ask_again(message)
    except Exception:
        bot.send_message(chat_id, 'Xatolik ! Qayta urinib kor',
                         reply_markup=generate_button())


def ask_again(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Yana tugmani bosing',
                     reply_markup=generate_button())



bot.polling(none_stop=True)

