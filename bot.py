import telebot
from telebot import types

def telegram_bot(token):

    chat_id = '@sendMessage12'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Анонимно")
    item2 = types.KeyboardButton("Не анонимно")

    markup.add(item1, item2)

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Выберите вид обращения", reply_markup=markup)

    @bot.message_handler(commands=['stop'])
    def sendTo(message):
        bot.send_message(message.chat.id, 'Спасибо за ваше заявление!\nЕсли хотите отправить сообщения нажмите /start')

    @bot.message_handler(content_types=['text'])
    def send(message):
        if message.text == 'Анонимно':

            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item3 = types.KeyboardButton('Книга жалоб и пожеланий')
            item4 = types.KeyboardButton('Личное обращения к начальнику департамента')

            markup1.add(item3, item4)

            bot.send_message(message.chat.id, 'Вы выбрали анонимное обращение, теперь выберите вид заявления',
                             reply_markup=markup1)
            name = 'Анонимный'
            bot.register_next_step_handler(message, jalob, name)

        elif message.text == 'Не анонимно':
            bot.send_message(message.chat.id, 'Вы выбрали не анонимное обращение\nНапишите свое ФИО')
            bot.register_next_step_handler(message, neonim)

        else:
            bot.send_message(message.chat.id, 'Извините, я непонимаю вас воспользуйтесь доступными командами!')
            bot.register_next_step_handler(message, send)

    def neonim(message):
        name = message.text
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item5 = types.KeyboardButton('Книга жалоб и пожеланий')
        item6 = types.KeyboardButton('Личное обращения к начальнику департамента')

        markup1.add(item5, item6)
        bot.send_message(message.chat.id, 'Теперь выберите вид заявления', reply_markup=markup1)
        bot.register_next_step_handler(message, jalob, name)

    def jalob(message, name):
        if message.text == 'Книга жалоб и пожеланий':
            bot.send_message(message.chat.id, 'Вы выбрали книгу жалоб\nНапишите свое сообщение!')
            bot.register_next_step_handler(message, previewno, name)
        elif message.text == 'Личное обращения к начальнику департамента':
            bot.send_message(message.chat.id, 'Вы выбрали личное обращение\nНапишите свое сообщение!')
            bot.register_next_step_handler(message, preview, name)
        else:
            bot.send_message(message.chat.id, 'Извините, я непонимаю вас воспользуйтесь доступными командами!')
            bot.register_next_step_handler(message, jalob, name)

    def preview(message, name):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item5 = types.KeyboardButton('Отправить')
        item6 = types.KeyboardButton('Отменить')

        markup1.add(item5, item6)
        text = message.text
        bot.send_message(message.chat.id, 'Предпросмтор:'
                         + '\nВид вашего заявления: Личное обращения к начальнику департамента'
                         + '\nВаше заявление:\n' + message.text
                         + '\nОтправитель: ' + name
                         + '\nЕсли все верно, нажмите кнопку <b>ОТПРАВИТЬ</b>, а если же сомневаетесь в правильности вашего заявления и хотите отредактировать нажмите кнопку <b>ОТМЕНИТЬ</b> и подайте заявление по новой ',
                         parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(message, sendMeslich, name, text)

    def previewno(message, name):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item5 = types.KeyboardButton('Отправить')
        item6 = types.KeyboardButton('Отменить')

        markup1.add(item5, item6)
        text = message.text
        bot.send_message(message.chat.id, 'Предпросмтор:'
                         + '\nВид вашего заявления: Книга жалоб и пожеланий'
                         + '\nВаше заявление:\n' + message.text
                         + '\nОтправитель: ' + name
                         + '\nЕсли все верно, нажмите кнопку <b>ОТПРАВИТЬ</b>, а если же сомневаетесь в правильности вашего заявления и хотите отредактировать нажмите кнопку <b>ОТМЕНИТЬ</b> и подайте заявление по новой ',
                         parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(message, sendMesjal, name, text)

    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item53 = types.KeyboardButton('/start')
    item63 = types.KeyboardButton('/stop')

    markup3.add(item53, item63)

    def sendMesjal(message, name, text):
        if message.text == 'Отправить':
            mes = "Книга жалоб и пожеланий\n\n" + text + "\n\n\t" + "Автор: " + name
            bot.send_message(chat_id, mes)
            bot.send_message(message.chat.id, 'Ваше заявление успешно отправлено!')
            bot.send_message(message.chat.id,
                             'Хотите еще отправить сообщения?\nЕсли да то нажмите <b>START</b> если нет то тогда <b>STOP</b>',
                             parse_mode='html', reply_markup=markup3)
        elif message.text == 'Отменить':
            bot.send_message(message.chat.id, 'Ваше заявление успешно отменено!')
            bot.send_message(message.chat.id, 'Чтобы заново начать нажмите <b>START</b> если нет то тогда <b>STOP</b>',
                             parse_mode='html', reply_markup=markup3)
        else:
            bot.send_message(message.chat.id, 'Извините, я непонимаю вас воспользуйтесь доступными командами!')
            bot.register_next_step_handler(message, sendMesjal, name, text)

    def sendMeslich(message, name, text):
        if message.text == 'Отправить':
            mes = "Личное обращения к начальнику департамента\n\n" + text + "\n\n\t" + "Автор: " + name
            bot.send_message(chat_id, mes)
            bot.send_message(message.chat.id, 'Ваше заявление успешно отправлено!')
            bot.send_message(message.chat.id,
                             'Хотите еще отправить сообщения?\nЕсли да то нажмите <b>START</b> если нет то тогда <b>STOP</b>',
                             parse_mode='html', reply_markup=markup3)
        elif message.text == 'Отменить':
            bot.send_message(message.chat.id, 'Ваше заявление успешно отменено!')
            bot.send_message(message.chat.id, 'Чтобы заново начать нажмите <b>START</b> если нет то тогда <b>STOP</b>',
                             parse_mode='html', reply_markup=markup3)
        else:
            bot.send_message(message.chat.id, 'Извините, я непонимаю вас воспользуйтесь доступными командами!')
            bot.register_next_step_handler(message, sendMeslich, text, name)

    bot.polling(none_stop=True)

if __name__ == '__main__':
    telegram_bot('5564555375:AAEP8WfcmuWZ3mjVzbb4eZvVKFY_i_SCyME')
