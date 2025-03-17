from telebot import TeleBot, types
import json

bot = TeleBot(token='ТОКЕН_ДОСТУПА', parse_mode='html') # создание бота

# Стикеры
START_STICKER = 'CAACAgIAAxkBAAENjGtn2GGb-45eD87nqDZionFWKfLugwAC_AAD9wLID-JKwmellSruNgQ'  # Замените на ID вашего стикера
SUCCESS_STICKER = 'CAACAgIAAxkBAAENjG9n2GG83yzE3tgp6gveEZHR-hxQzQAC9wAD9wLID9CX3j-K0TwONgQ'  # Замените на ID вашего стикера


# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем стикер
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=START_STICKER
    )
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет! Я умею проверять JSON и форматировать его в красивый текст\nВведи JSON в виде строки:', # текст сообщения
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    try:
        # пытаемся распарсить JSON из текста сообщения
        payload = json.loads(message.text)
    except json.JSONDecodeError as ex:
        # при ошибке взникнет исключение 'json.JSONDecodeError'
        # преобразовываем исключение в строку и выводим пользователю
        bot.send_message(
            chat_id=message.chat.id,
            text=f'При обработке произошла ошибка:\n<code>{str(ex)}</code>'
        )
        # выходим из функции
        return
    
    # если исключения не возникло - значит был введен корректный JSON
    # форматируем его в красивый текст :) (отступ 2 пробела на уровень, сортировать ключи по алфавиту)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'JSON:\n<code>{text}</code>'
    )
    # отправляем стикер после успешной обработки JSON
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=SUCCESS_STICKER
    )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()