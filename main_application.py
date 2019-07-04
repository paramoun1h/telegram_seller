from database import Operation
from qiwi import Qiwi
from config import token_telegram, token_qiwi, number
import telebot
from telebot import types

bot = telebot.TeleBot(token_telegram)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    action = types.KeyboardButton(text="Проверить")
    keyboard.add(action)
    bot.send_message(message.chat.id,
                     f"Для покупки аккаунта вам необходимо отправить 100р на данный"
                     f" qiwi кошелек {number} с комментарием {message.from_user.id}."
                     f" После чего нажать на кнопку 'Проверить' и ожидать последующей "
                     f"информации"
                     , reply_markup=keyboard)


@bot.message_handler(regexp="Проверить")
def handle_message(message):
    check = Qiwi(token_qiwi)
    elements_to_check = check.find_pay(str(message.from_user.id), check.get_history())
    # print(elements_to_check)
    if elements_to_check['total']['amount'] == 10 and elements_to_check['total']['currency'] == 643:
        my_database = Operation()
        if my_database.select(str(message.from_user.id), elements_to_check['date']):
            bot.send_message(message.chat.id, f'Новых платежей от вас не поступало')
        else:
            my_database.commit(str(message.from_user.id),elements_to_check['date'])
            bot.send_message(message.chat.id, f'Логин:{12}\nПароль:{1}')
    else:
        bot.send_message(message.chat.id, 'Ожидаются данный')




bot.polling()
