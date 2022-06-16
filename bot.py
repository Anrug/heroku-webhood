import telebot
import smtplib

from email.mime.text import MIMEText
from telebot import types

import os
from Flask import Flask, request

TOKEN = '5408185153:AAHdepDiOhlnXoRpKR8u16Eb9nBo7HP2NqY'
APP_URL = f'https://angurheroku.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Анонимно")
item2 = types.KeyboardButton("Не анонимно")

markup.add(item1, item2)

def send_email(mes, message):
    sender = "telegram.bot.96@mail.ru"
    password = "Xg5kGfr4dcjCzpCLwwXv"

    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()

    try:
        server.login(sender,password)
        msg = MIMEText(message)
        msg["Subject"] = mes
        server.sendmail(sender, "telegram.bot.96@mail.ru", msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


Mes = ['Анонимный']

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, "Здравствуйте, Я - бот который принимает жалобы, пожелания и личные обращения", 
    parse_mode='html', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def send(message):
    if message.text == 'Анонимно':

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item3 = types.KeyboardButton('Книга жалоб')
        item4 = types.KeyboardButton('Личное обращения')

        markup1.add(item3, item4)

        bot.send_message(message.chat.id, 'Вы выбрали анонимное сообщение, теперь выберите вид обращение', reply_markup=markup1)
        Mes[0] = 'Анонимный'
        bot.register_next_step_handler(message, jalob)

    elif message.text == 'Не анонимно':
        bot.send_message(message.chat.id, 'Вы выбрали не анонимное сообщение\n Напишите Фамилия Имя Очество')
        bot.register_next_step_handler(message, neonim)

    else:
        bot.send_message(message.chat.id, 'Error')
        

def neonim(message):
    Mes[0] = message.text
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item5 = types.KeyboardButton('Книга жалоб')
    item6 = types.KeyboardButton('Личное обращения')

    markup1.add(item5, item6)
    bot.send_message(message.chat.id, 'Теперь выберите вид обращения', reply_markup=markup1)
    bot.register_next_step_handler(message, jalob)


def jalob(message):
    if message.text == 'Книга жалоб':
        bot.send_message(message.chat.id, 'Вы выбрали книгу жалоб\n Напишите свое сообщение!')
        bot.register_next_step_handler(message, sendMesjal)
    elif message.text == 'Личное обращения':
        bot.send_message(message.chat.id, 'Вы выбрали личное обращение\n Напишите свое сообщение!')
        bot.register_next_step_handler(message, sendMeslich)
    
    
def sendMesjal(message):
    print(send_email(mes = 'Книга жалоб', message=message.text + "\n\n\t" + "Автор: " + Mes[0]))
    bot.send_message(message.chat.id, 'Ваше сообщение успешно отправлено!', reply_markup=markup)
    bot.register_next_step_handler(message, start)

def sendMeslich(message):
    print(send_email(mes = 'Личное обращения', message=message.text + "\n\n\t" + "Автор: " + Mes[0]))
    bot.send_message(message.chat.id, 'Ваше сообщение успешно отправлено!', reply_markup=markup)
    bot.register_next_step_handler(message, start)

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))