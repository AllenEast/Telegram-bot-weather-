
import requests
import telebot

API_KEY = '6418b539e0697f54de8a3df65ebe9444'
bot_token = '6480859175:AAH-8PcaiPB6S2eRWvYBqrN6eCVdbByfQs4'

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Weather Bot! Please enter the city name to get the weather information.")


@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url).json()

    if response['cod'] == 200:
        weather_description = response['weather'][0]['description']
        temperature = response['main']['temp']
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']

        reply_text = f"Weather in {city}: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s"
    else:
        reply_text = "Sorry, couldn't fetch the weather information for that city."

    bot.reply_to(message, reply_text)



bot.polling(none_stop=True)

