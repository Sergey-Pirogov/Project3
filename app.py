import telebot
from config import keys, TOKEN
from exceptions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])            #Информация при запуске бота
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n<Имя валюты>\
<В какую валюту перевести> \
<Колличество переводимой валюты> \n Увидеть список всех доступных валют : /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])                   #Информация по доступным валютам
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text= '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])              #Проверка, обработка и отображение результатов значений
def covert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Введите 3 параметра\n В формате \n<Имя валюты>\
<В какую валюту перевести> \
<Колличество переводимой валюты> \n Увидеть список всех доступных валют : /values")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
        convert = CryptoConverter.convert(quote, base, "1")

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось распознать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}\n Курс конвертации: {convert}'
        bot.send_message(message.chat.id, text)



bot.polling()
