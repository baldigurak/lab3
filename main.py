""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7551754051:AAFW5uV1W2UzxdKAqLj8K_vCxykqnYE0iss'

OPENWEATHER_API_KEY='bde1d8a082d24aa304ea220d5fe53848'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Доброе время суток.\nЯ могу показать погоду в Самаре\n")

    @dp.message_handler(commands=['weather'])
    async def send_weather(message: types.Message):

        weather_info = get_weather_samara()

        await message.reply(weather_info)

def get_weather_samara():
    city = "Самара"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        weather_desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        return (
            f"🌤 Погода в {city_name}, {country}:\n"
            f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"Описание: {weather_desc}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
    else:
        return '❌ Не удалось получить данные о погоде.'

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)