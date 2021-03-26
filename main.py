import telebot
from telebot import types
import config
import requests
name = ' '
age = 0
bot = telebot.TeleBot(config.token)

response = requests.get(config.url).json()



@bot.message_handler(commands=['usd'])
def keyboard1(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('USD')
    btn2 = types.KeyboardButton('EUR')
    btn3 = types.KeyboardButton('RUR')
    btn4 = types.KeyboardButton('BTC')
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id,
                               "Хочешь узнать наличный курс основных валют за 2014 год?\nНажми на нужную тебе валюту в появившейся клавиатуре👇", reply_markup=markup)
    bot.register_next_step_handler(msg, process_coin_step)

def process_coin_step(message):
        try:
            markup = types.ReplyKeyboardRemove(False)

            for coin in response:
                if (message.text == coin['ccy']):
                    bot.send_message(message.chat.id, printCoin(coin['buy'], coin['sale']),
                                     reply_markup=markup, parse_mode="Markdown")

        except Exception as e:
            bot.reply_to(message, 'ooops!')


def printCoin(buy, sale):
        '''Вывод курса пользователю'''
        return "💰 *Курс покупки:* " + str(buy) + "\n💰 *Курс продажи:* " + str(sale)


@bot.message_handler(content_types=['text', 'document', 'audio'])
def echo_all(message):
    if message.text.lower() == '/start':
        bot.send_message(message.from_user.id, 'Приветик! \nНапиши /reg чтобы познакомиться поближе')
    elif  message.text.lower() == 'Привет':
        bot.send_message(message.from_user.id, 'Приветик!')
    elif message.text.lower() == '/help':
            bot.send_message(message.from_user.id, 'Мои команды:\n/usd - посмотреть курс основных валют(2014год) \n/btc - список актуальных бирж криптовалют ')
    elif message.text.lower() == '/reg':
        bot.send_message(message.chat.id, 'Привет! Давай знакомиться! Как тебя зовут?')
        bot.register_next_step_handler(message, reg_name)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    age = message.text
    while age == 0:
        try:
                age = int(message.text)
        except Exception:
            bot.send_message(message, 'Введите цифры!!')


    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text = 'Нет', callback_data='no')
    keyboard.add(key_no)

    question =  'Тебе ' + str(age) + ' лет. И тебя зовут: ' + name +'?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
        if call.data == 'yes':
            bot.send_message(call.message.chat.id, 'Приятно познакомиться. Ты все сделал верно☺\nЕсли хочешь посмотреть список всех моих команд, напиши /help', )
        elif call.data -- 'no':
            bot.send_message(call.message.chat.id, 'Упс... Попробуй еще раз')
            bot.send_message(call.message.chat.id, 'Привет! Давай знакомиться! Как тебя зовут?')
            bot.send_message(call.message, reg_name)








if __name__== '__main__':
    bot.polling(none_stop=True)