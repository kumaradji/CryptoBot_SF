import requests
import json

from config import exchanges, APIKEY


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def convert(base: str, target: str, amount: str):
        try:
            base_code = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            target_code = exchanges[target.lower()]
        except KeyError:
            raise APIException(f'Валюта {target} не найдена!')

        if base_code == target_code:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/{APIKEY}/pair/{target_code}/{base_code}/{amount}")
        resp = json.loads(r.content)
        print(resp)
        new_price = resp['conversion_rate'] * amount
        new_price = round(new_price, 3)
        message = f'Цена {amount} {base} в {target} : {new_price}'
        return message

