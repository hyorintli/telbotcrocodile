import telebot
from telebot import types
import random

bot = telebot.TeleBot("5779665023:AAG8xpRzi2zhGkzbKduEKiiM8p1Mdp-bzOo")

answer = ""  # правильна відповідь
words = []  # список обраних слів
player = ""  # ведучий гравець
scoring = {}  # словник (нікнейм гравця: кількість балів)


# зчитує слова за файлу та перемішує їх
def reset_words(fname):
    global words

    f = open(f"{fname}.txt", "r", encoding="UTF-8")
    words = f.read().split("\n")
    f.close()
    random.shuffle(words)  # перемішує список слів


@bot.message_handler(commands=["start"])
def start(message):
    global player

    markup_inline = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text="природа", callback_data="nature")
    btn2 = types.InlineKeyboardButton(text="техніка", callback_data="technical")

    markup_inline.add(btn1)
    markup_inline.add(btn2)

    player = message.from_user.username
    bot.send_message(message.chat.id, text=f"Привіт {message.from_user.first_name} обери тему для гри 🎮",
                     reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def сheck_inline_keyboard(call):
    global answer, words, player

    if call.data == "show":
        if call.from_user.username == player:
            bot.answer_callback_query(call.id, text=answer, show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="неможна ❌", show_alert=True)
    elif call.data == "next":
        markup_inline = types.InlineKeyboardMarkup()
        answer = words.pop()

        btn1 = types.InlineKeyboardButton(text="подивитись слово 👀", callback_data="show")
        btn2 = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")

        markup_inline.add(btn1)
        markup_inline.add(btn2)
        player = call.from_user.username
        bot.send_message(call.message.chat.id, text=f"Зараз пояснює слово  {call.from_user.first_name}  🧠",
                         reply_markup=markup_inline)

        # answer = words.pop()
        #
        # if call.from_user.username == player:
        #     bot.answer_callback_query(call.id, text=answer, show_alert=True)
        # else:
        #     bot.answer_callback_query(call.id, text="неможна ❌", show_alert=True)
    elif call.data == "nature":
        markup_inline = types.InlineKeyboardMarkup()
        reset_words("nature")
        answer = words.pop()

        btn1 = types.InlineKeyboardButton(text="подивитись слово 👀", callback_data="show")
        btn2 = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")

        markup_inline.add(btn1)
        markup_inline.add(btn2)
        player = call.from_user.username
        bot.send_message(call.message.chat.id, text=f"Зараз пояснює слово {call.from_user.first_name} 🧠",
                         reply_markup=markup_inline)
    elif call.data == "technical":
        markup_inline = types.InlineKeyboardMarkup()
        reset_words("technical")
        answer = words.pop()

        btn1 = types.InlineKeyboardButton(text="подивитись слово 👀", callback_data="show")
        btn2 = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")

        markup_inline.add(btn1)
        markup_inline.add(btn2)
        player = call.from_user.username
        bot.send_message(call.message.chat.id, text=f"Зараз пояснює слово  {call.from_user.first_name}  🧠",
                         reply_markup=markup_inline)


@bot.message_handler(content_types=["text"])
def check_word(message):
    global scoring

    if message.text.lower() == answer.lower() and player != message.from_user.username:
        markup_inline = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")

        if message.from_user.username in scoring.keys(): # якщо нік гравця є в словнику scoring
            scoring[message.from_user.username] += 1
        else:
            scoring[message.from_user.username] = 1

        if scoring[message.from_user.username] >= 10:
            bot.send_message(message.chat.id,
                             text=f"гравець {message.from_user.username} переміг 🎀",
                             reply_markup=markup_inline)
        else:
            markup_inline.add(btn1)
            bot.send_message(message.chat.id, text=f"ти відгадав, у {message.from_user.username} "
                                                   f"{scoring[message.from_user.username]} балів",
                             reply_markup=markup_inline)


bot.polling(none_stop=True)
