import telebot
# from telebot import types
import random

user_sweets = 0
sweets = 0
bot_win = 0
smart_bot_choose = -1
whose_move = ''
bot = telebot.TeleBot("5897991903:AAF3jvA8gx6jOhtJrEVv1B6qboK_-Pgh63o")


@bot.message_handler(commands=['start'])  # вызов функции по команде в списке
def start(message):
    global sweets
    global whose_move
    sweets = 221
    whose_move = random.choice(['user', 'bot'])
    bot.send_message(message.chat.id, f"Всего: {sweets} конфет")
    bot.send_message(message.chat.id, f"Первым ходит {whose_move} ")
    if whose_move == 'user':
        bot.send_message(message.chat.id, f"Введите количество не больше 28")
        bot.register_next_step_handler(message, user_input)
    else:
        bot.send_message(
            message.chat.id, f'Выберите бота\n /bot \n /smart_bot')
    # controller(message)


@bot.message_handler(commands=['bot'])
def bot_bot(message):
    global user_sweets
    global smart_bot_choose
    if smart_bot_choose == -1:
        smart_bot_choose = 0
    user_sweets = random.randint(1, 28)
    get_count(message)


@bot.message_handler(commands=['smart_bot'])
def smart_bot(message):
    global sweets
    global user_sweets
    global smart_bot_choose
    if smart_bot_choose == -1:
        smart_bot_choose = 1
    tmp = sweets//29
    user_sweets = sweets-29*tmp
    if user_sweets == 0:
        user_sweets = random.randint(1, 28)
    get_count(message)


def controller(message):
    global sweets
    global whose_move
    if sweets <= 0:
        bot.send_message(message.chat.id, f'Выиграл {whose_move}')
        start(message)
    else:
        if whose_move == 'bot':
            whose_move = 'user'
            bot.send_message(
                message.chat.id, f"Введите количество не больше 28")
            bot.register_next_step_handler(message, user_input)
        else:
            whose_move = 'bot'
            if smart_bot_choose == -1:
                bot.send_message(
                    message.chat.id, f'Выберите бота\n /bot \n /smart_bot')
            elif smart_bot_choose == 0:
                bot_bot(message)
            elif smart_bot_choose == 1:
                smart_bot(message)


def get_count(message):
    global sweets
    sweets = sweets - user_sweets
    bot.send_message(
        message.chat.id, f'{whose_move} взял {user_sweets} конфет')
    bot.send_message(message.chat.id, f"осталось {sweets}")
    controller(message)


def user_input(message):
    global user_sweets
    user_sweets = int(message.text)
    get_count(message)


bot.infinity_polling()
