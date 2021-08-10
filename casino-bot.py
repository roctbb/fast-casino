import random
import time
from threading import Thread

from telebot import TeleBot
from config import telegram_token
from helpers import generate_keyboard
from bank_api import ask_money, verify_transaction, send_money

bot = TeleBot(telegram_token)
options = ['️1', '2', '3']  #
temp = {}
bets = {}


def recode(option):
    return option.replace('1', '🐷').replace('2', '️🍑').replace('3', '❤️')


def generate_option():
    return ''.join(random.choice(options) for i in range(3))


def run_game(message):
    msg = bot.send_message(message.chat.id, "Запускаем машину судьбы...")
    time.sleep(1)
    old_option = ""
    for i in range(10):
        option = generate_option()
        while option == old_option:
            option = generate_option()
        old_option = option

        bot.edit_message_text(recode(option), message.chat.id, msg.message_id)
        time.sleep(0.4)

    if old_option == '111':
        bot.send_message(message.chat.id, "Офигенная тема! 20x!!!")
        print(send_money(message.chat.id, bets[message.chat.id] * 20, "Выигрыш в казино."))
        bot.send_message(message.chat.id, "Перевели деньги. Еще раз?")
    elif old_option == '️222':
        bot.send_message(message.chat.id, "5x!!!")
        print(send_money(message.chat.id, bets[message.chat.id] * 10, "Выигрыш в казино."))
        bot.send_message(message.chat.id, "Перевели деньги. Еще раз?")
    elif old_option == '333':
        bot.send_message(message.chat.id, "3x!!!")
        print(send_money(message.chat.id, bets[message.chat.id] * 5, "Выигрыш в казино."))
        bot.send_message(message.chat.id, "Перевели деньги. Еще раз?")
    else:
        bot.send_message(message.chat.id, "В этот раз не судьба. Еще раз?")

    send_menu(message)


def send_menu(message):
    keyboard = generate_keyboard(["💸 10", "💸 50", "💸 100"])
    msg = bot.send_message(message.chat.id, "Делаешь ставку? Смелей!", reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_pay)


def ask_code(message):
    msg = bot.send_message(message.chat.id, "Пришли код подтверждения...")
    bot.register_next_step_handler(msg, process_code)


def process_code(message):
    try:
        code = int(message.text)
    except:
        ask_code(message)
        return

    result = verify_transaction(temp[message.chat.id], code)

    if 'error' in result:
        bot.send_message(message.chat.id, "Не удалось сделать ставку, банк вернул ошибку - {}.".format(result['error']))
        send_menu(message)
    else:
        bot.send_message(message.chat.id, "Ставка принята!")
        t = Thread(target=run_game, args=(message,))
        t.start()


def process_pay(message):
    amount = None

    if "100" in message.text:
        amount = 100
    elif "50" in message.text:
        amount = 50
    else:
        amount = 10

    if amount:
        bets[message.chat.id] = amount
        transaction = ask_money(message.chat.id, amount, 'Ставка в казино "У Роста"')

        if 'transaction_id' not in transaction:
            bot.send_message(message.chat.id,
                             "Не удалось сделать ставку, банк вернул ошибку - {}.".format(transaction['error']))
            send_menu(message)
        else:
            ask_code(message)
            temp[message.chat.id] = transaction['transaction_id']
    else:
        send_menu(message)


@bot.message_handler(content_types=['text'])
def start(message):
    send_menu(message)


bot.polling(none_stop=True)
