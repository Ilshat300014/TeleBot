from config import token
from extensions import ReqiestAPI
from extensions import APIExceptionError
import telebot

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start','help'])
def explain(message):
    text = 'Приветствую!\n Я возвращаю цену на определённое количество валюты (евро, доллар или рубль). ' \
           'Для этого набери команду в виде <имя валюты, цену которую хочешь узнать> ' \
           '<имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>. ' \
           'Например, доллар рубль 1. Ответом на такой запрос будет цена в рублях за 1 доллар. ' \
           'При вводе команды /start или /help выведу данную инструкцию. ' \
           'При вводе команды /value выведу информацию о всех доступных валютах.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['value',])
def valutes(message):
    s = 'Доллар\nЕвро\nРубль'
    bot.send_message(message.chat.id, s)

@bot.message_handler(content_types=['text'])
def ask_to_photo(message):
    l = message.text.split()
    valutes = ['доллар', 'евро', 'рубль']
    try:
        base = l[0]
        quote = l[1]
        amount = l[2]
    except IndexError:
        error = APIExceptionError(error_enter=True)
        bot.send_message(message.chat.id, error)
        raise error
    else:
        if amount.isdigit() and base.lower() in valutes and quote.lower() in valutes:
                t = ReqiestAPI.get_price(base, quote, float(amount))
        else:
            error = APIExceptionError(base, quote, amount)
            bot.send_message(message.chat.id, error)
            raise error
    bot.send_message(message.chat.id, t)

bot.polling(none_stop=True)
