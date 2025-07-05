import telebot
from tokenid import token
import random
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
        bot.reply_to(message, "Привет! Я EcoLev_Bot, Я Буду Отвечать На Твои Вопросы По Экологии. Подробности: Напиши Команду: /help")

@bot.message_handler(commands=['help'])
def send_welcome(message):
        bot.reply_to(message, "Случайная картинка факт про экологию - /image \n Вопросы: \n Что такое экология? - /ecology_what_is_it, \n Что такое глобальное поетпление? - /global_warming_what_is_it, \n Как улучшить экологию? -  /how_to_respect_the_ecology")

@bot.message_handler(commands=['ecology_what_is_it'])
def send_welcome(message):
        bot.reply_to(message, "Экология — это познание экономики природы, одновременное исследование всех взаимоотношений живого с органическими и неорганическими компонентами окружающей среды… Одним словом, экология — это наука, изучающая все сложные взаимосвязи в природе, рассматриваемые Дарвином как условия борьбы за существование.")

@bot.message_handler(commands=['global_warming_what_is_it'])
def send_welcome(message):
        bot.reply_to(message, "Глобальное потепление — распространенное название изменения климата, которое идет уже около двух веков. ООН определяет это явление как долгосрочные изменения температуры и погодных условий, вызванное естественными причинами, вроде активности Солнца, и антропогенными — из-за действий человека.")

@bot.message_handler(commands=['how_to_respect_the_ecology'])
def send_welcome(message):
        bot.reply_to(message, "Чтобы соблюдать экологию, нужно минимизировать воздействие на окружающую среду, начиная с простых повседневных действий. Это включает в себя сокращение отходов, разумное потребление ресурсов, таких как вода и электроэнергия, и заботу о природе во время отдыха на природе.")

@bot.message_handler(commands=['image'])
def send_mem(message):
    img_name = random.choice(os.listdir("images"))
    with open(f'images/{img_name}', 'rb') as f:  
        bot.send_photo(message.chat.id, f)

bot.polling()