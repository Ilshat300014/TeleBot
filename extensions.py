import requests
import json

class ReqiestAPI:
    @staticmethod
    def get_price(base, quote, amount):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        responce = requests.get(url) # .json()['Valute']
        data = json.loads(responce.text)
        valutes = data['Valute']
        usd_value = float(valutes["USD"]["Value"])
        eur_value = float(valutes["EUR"]["Value"])
        data = {'доллар': usd_value,
                'евро': eur_value,
                'рубль': 1}
        req_value = (data[base] * amount) / data[quote]
        result = round(req_value, 2)
        return result

class APIExceptionError(Exception):
    valutes = ['доллар', 'евро', 'рубль']
    def __init__(self, base=None, quote=None, amount=None, error_enter = False):
        self.base = base
        self.quote = quote
        self.amount = amount
        if not all([self.base, self.quote, self.amount]) or error_enter:
            self.text = 'Неверный ввод. Необходимо ввести запрос в виде:\n' \
                '<Имя валюты, цену которую хочешь узнать> ' \
                '<Имя валюты в которой надо узнать цену первой валюты> ' \
                '<Количество первой валюты>'
        elif self.base.lower() not in self.valutes:
            self.text = f'Неопознанный вид валюты "{self.base}". Доступные валюты: доллар, евро, рубль'
        elif self.quote.lower() not in self.valutes:
            self.text = f'Неопознанный вид валюты "{self.quote}". Доступные валюты: доллар, евро, рубль'
        elif not self.amount.isdigit():
            self.text = 'Неправильный ввод. Параметр <Количество первой валюты> должен быть цифрой'

    def __str__(self):
        return self.text




