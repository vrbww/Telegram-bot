# подключение библиотек
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: вставить свой токен
TOKEN = ' '
bot = TeleBot(TOKEN, parse_mode='html')
# библиотека для генерации тестовых ФИО
# указываем язык - русский
faker = Faker('ru_RU') 

# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="💼 Мой сайт-визитка на Github")
)
# второй ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="✉️ Написать мне в лс")
)
# третий ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="🤖 Сгенерировать тестовые данные")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # не забываем прикрепить объект клавиатуры к сообщению
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭто бот для генерации тестовых пользователей.\nЯ создал его в помощь себе и как дополнение к сайту-визитке. Приятного пользования! 🙂",
        reply_markup=main_menu_reply_markup
    )


# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    if message.text == "💼 Мой сайт-визитка на Github":
        bot.send_message(
            chat_id=message.chat.id,
            text="Переход на Git ⬇️",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="https://vrbww.github.io/",
            reply_markup=main_menu_reply_markup
        )
    elif message.text == "✉️ Написать мне в лс":
        bot.send_message(
            chat_id=message.chat.id,
            text="Переход на мой TG-профиль ⬇️",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="https://t.me/SMR_Dmitry_Vorobyew",
            reply_markup=main_menu_reply_markup
        )
    elif message.text == "🤖 Сгенерировать тестовые данные":
        bot.send_message(
            chat_id=message.chat.id,
            text="Сколько тестовых пользователей сгенерировать?",
            reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).row(
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="5"),
                types.KeyboardButton(text="10")
            )
        )
    else:
        payload_len = 0
        if message.text == "1":
            payload_len = 1
        elif message.text == "2":
            payload_len = 2
        elif message.text == "5":
            payload_len = 5
        elif message.text == "10":
            payload_len = 10
        else:
            bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
            return

        # генерируем тестовые данные для выбранного количества пользователей
        # при помощи метода simple_profile
        total_payload = []
        for _ in range(payload_len):
            user_info = faker.simple_profile()
            user_info['phone'] = f'+7{faker.msisdn()[3:]}'
            # при помощи библиотеки secrets генерируем пароль
            user_info['password'] = token_urlsafe(10)
            total_payload.append(user_info)

        # сериализуем данные в строку
        payload_str = json.dumps(
            obj=total_payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            default=str
        )

        # отправляем результат
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
            f"{payload_str}</code>"
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
            reply_markup=main_menu_reply_markup
        )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()