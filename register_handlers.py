import telebot
from info import *
from gpt import *
import sqlite3
from datetime import datetime
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton



bot = telebot.TeleBot(TOKEN)


def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text.lower() == "написать поздравление🎉") 
    def first(message):
        print("first")
        user_id = message.from_user.id
        user_name = message.from_user.username
        logging.info(f"Пользователь с id - {user_id} использовал кнопку 'написать поздравление🎉'")
        bot.send_message(message.chat.id, "Напиши для кого будет поздравление:")
        bot.register_next_step_handler(message, name)
        
    def name(message):
        print("name")
        user_id = message.from_user.id
        user_name = message.from_user.username
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        sql_query = "UPDATE users_data SET task = ? WHERE user_id = ?;"
        cur.execute(sql_query, (f"Напиши поздравление для {message.text}", user_id))
        connection.commit()
        connection.close()
        bot.send_message(message.chat.id, "Напиши с чем ты хочешь его поздравить:")
        bot.register_next_step_handler(message, occasion)

    def occasion(message):
        print("occasion")
        user_id = message.from_user.id
        user_name = message.from_user.username
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        task = cur.execute(f'''SELECT task FROM users_data WHERE user_id = {user_id}''').fetchone()[0]
        sql_query = "UPDATE users_data SET task = ? WHERE user_id = ?;"
        cur.execute(sql_query, (f"{task}. Поздравь его с {message.text}", user_id))
        connection.commit()
        connection.close()
        count_tokens(message)
    