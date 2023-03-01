import requests
import json

from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def convert(base: str, sym: str, amount: str):
        try:
            quote_ticker = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            base_ticker = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f'Валюта {sym} не найдена!')

        if quote_ticker == base_ticker:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}")
        resp = json.loads(r.content)
        new_price = resp['rates'][base_ticker] * amount
        new_price = round(new_price, 3)
        message = f'Цена {amount} {base} в {sym} : {new_price}'
        return message
