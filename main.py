import telebot
import pprint
from telebot import types
import googletrans
from googletrans import Translator
import requests as req
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv

load_dotenv()


class Compliment():
    def __init__(self):
        self.text = req.get("https://complimentr.com/api").json()["compliment"]

    def get_compliment(self):
        translator = Translator()
        str_to_return = translator.translate(self.text, src='en', dest='ru').text
        return str_to_return


class Weather():
    def __init__(self, lat, lon):
        WeatherId = os.getenv("WeatherId")
        self.weather = req.get("https://api.openweathermap.org/data/2.5/weather?lat=" +
                              str(lat) + "&lon=" + str(lon) + "&appid=" + WeatherId)

    def get_weather(self):
        translator = Translator()
        str_to_return = "Погода: " + translator.translate(self.weather.json()["weather"][0]["description"],
                                                          src='en', dest='ru').text + "\n"
        str_to_return += "Tемпература: " + str(self.weather.json()["main"]["temp"] - 273.15) + " градусов Цельсия\n"
        str_to_return += "Cкорость ветра: " + str(self.weather.json()["wind"]["speed"]) + " м/c"
        return str_to_return

class Recipe:
    def __init__(self):
        recipe = req.get("https://www.themealdb.com/api/json/v1/1/random.php").json()['meals'][0]
        self.name = recipe['strMeal']
        self.instructions = recipe['strInstructions']
        self.ingredients = ''
        for i in range(1, 21):
            if recipe["strIngredient" + str(i)] != '' and recipe["strMeasure" + str(i)] != '':
                self.ingredients += recipe["strIngredient" + str(i)] + "   " + recipe["strMeasure" + str(i)] + "\n"

    def get_recipe(self):
        translator = Translator()
        str_to_return = translator.translate(self.name, src='en', dest='ru').text + "\n\n"
        str_to_return += translator.translate(self.instructions, src='en', dest='ru').text + "\n\n"
        str_to_return += translator.translate(self.ingredients, src='en', dest='ru').text + "\n\n"
        return str_to_return


class Anecdote:
    def __init__(self):
        self.text = req.get("http://rzhunemogu.ru/RandJSON.aspx?CType=1").text[12:-3]

    def get_anecdote(self):
        return self.text

TBotToken = os.getenv("TBotToken")
botTimeWeb = telebot.TeleBot(TBotToken)


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"{message.from_user.first_name}, привет!\nЯ - супер крутой телеграм бот для домохозяек," \
                 f" что ты хочешь, солнышко?"
    markup = types.ReplyKeyboardMarkup()

    button_anecdote = types.KeyboardButton(text='Анекдот')
    markup.add(button_anecdote)

    button_recipe = types.KeyboardButton(text='Рецепт')
    markup.add(button_recipe)

    button_weather = types.KeyboardButton(text='Погода в Омске')
    markup.add(button_weather)

    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@botTimeWeb.message_handler(content_types=['text'])
def func(message):
    if message.text == "Анекдот":
        second_mess = Anecdote().get_anecdote()
        markup = types.InlineKeyboardMarkup()
        button_compliment = types.InlineKeyboardButton(text='Комплимент', callback_data='compliment')
        markup.add(button_compliment)
        botTimeWeb.send_message(message.chat.id, second_mess, parse_mode='html', reply_markup=markup)

    if message.text == "Рецепт":
        recipe = Recipe()
        second_mess = "Рецепт \n\n" + recipe.get_recipe()
        markup = types.InlineKeyboardMarkup()
        button_compliment = types.InlineKeyboardButton(text='Комплимент', callback_data='compliment')
        markup.add(button_compliment)
        botTimeWeb.send_message(message.chat.id, second_mess, parse_mode='html', reply_markup=markup)

    if message.text == "Погода в Омске":
        second_mess = "В каком районе Омска вас интересует погода?"
        markup = types.InlineKeyboardMarkup()

        button_kirovsky = types.InlineKeyboardButton(text='Кировский', callback_data='kirovsky')
        markup.add(button_kirovsky)

        button_sovetsky = types.InlineKeyboardButton(text='Советский', callback_data='sovetsky')
        markup.add(button_sovetsky)

        button_central = types.InlineKeyboardButton(text='Центральный', callback_data='central')
        markup.add(button_central)

        button_oktyabrsky = types.InlineKeyboardButton(text='Октябрьский', callback_data='oktyabrsky')
        markup.add(button_oktyabrsky)

        button_leninsky = types.InlineKeyboardButton(text='Ленинский', callback_data='leninsky')
        markup.add(button_leninsky)

        botTimeWeb.send_message(message.chat.id, second_mess, parse_mode='html', reply_markup=markup)


@botTimeWeb.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.message:
        if function_call.data == "kirovsky":
            second_mess = Weather(54.989522, 73.257822).get_weather()
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, parse_mode='html')

        if function_call.data == "sovetsky":
            second_mess = Weather(55.032575, 73.278744).get_weather()
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, parse_mode='html')

        if function_call.data == "central":
            second_mess = Weather(55.01533, 73.42354).get_weather()
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, parse_mode='html')

        if function_call.data == "oktyabrsky":
            second_mess = Weather(54.954765, 73.442073).get_weather()
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, parse_mode='html')

        if function_call.data == "leninsky":
            second_mess = Weather(54.899079, 73.378687).get_weather()
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, parse_mode='html')

        if function_call.data == "compliment":
            second_mess = Compliment().get_compliment()
            botTimeWeb.send_message(function_call.message.chat.id, second_mess, parse_mode='html')


botTimeWeb.infinity_polling()
