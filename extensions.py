import requests
import json

from config import exchanges, APIKEY


# Класс с исключениями API
class APIException(Exception):
    pass


# Класс конвертирования валют с выполнением запроса на API https://app.exchangerate-api.com/
class Convertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str) -> str:
        try:
            base_code = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена!')

        try:
            target_code = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        if base_code == target_code:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        # Получение необходимого JSON для обработки
        r = requests.get(f"https://v6.exchangerate-api.com/v6/{APIKEY}/pair/{target_code}/{base_code}/{amount}")
        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * amount
        new_price = round(new_price, 3)
        message = f'Цена {amount} {quote} в {base} : {new_price}'
        return message
