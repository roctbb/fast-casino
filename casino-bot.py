from telebot import TeleBot, types
from config import telegram_token
from helpers import generate_keyboard

bot = TeleBot(telegram_token)
users = {}

def process_pay(message):
    amount = None

    if "10" in message.text:
        amount = 10
    elif "50" in message.text:
        amount = 50
    else:
        amount = 100

@bot.message_handler(content_types=['text'])
def start(message):
    keyboard = generate_keyboard(["💸 10", "💸 50", "💸 100"])
    msg = bot.send_message("Делаешь ставку? Смелей!", reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_pay)