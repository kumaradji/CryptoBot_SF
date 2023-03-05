import telebot
import traceback

from config import exchanges, TOKEN
from extensions import APIException, Convertor

bot = telebot.TeleBot(TOKEN)


# Обрабатывает сообщения, содержащие команды /'start' и /'help'.
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)


# Обрабатывает сообщения, содержащие команды /'values'.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


# Конвертирует валюту и обрабатывает исключения
@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    val = message.text.split(' ')
    answer = Convertor.get_price(*val)

    try:
        if len(val) != 3:
            raise APIException('Неправильно указаны параметры /start')
    except APIException as e:
        bot.reply_to(message, f'Ошибка в команде:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n{e}')
    else:
        bot.reply_to(message, answer)


bot.polling()
