import config
from DataBase import Data
import telebot
from info import *
from gpt import *
from register_handlers import *
from fusion import *
import sqlite3
from datetime import datetime
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os.path


bot = telebot.TeleBot(TOKEN)
Data().create_table(['id', 'user_id', 'user_name', 'user_role', 'tokens', 'request', 'task'], ['INTEGER PRIMARY KEY', 'INTEGER', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="a",
    encoding='utf-8',
)


MAX_USERS = 50
MAX_TOKENS = 120

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Написать открытку🖼️').add("Написать поздравление🎉").add("Написать тост🥂").add("Написать конкурс🎈")

def is_limit_users():
        global MAX_USERS
        connection = sqlite3.connect('/home/student/congratulations_bot/database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT DISTINCT user_id FROM users_data;')
        count = 0 
        for i in result: 
            count += 1 
        connection.close()
        return count >= MAX_USERS  




@bot.message_handler(commands=["start"])
def welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    logging.info(f"Пользователь с id - {user_id} использовал комманду /start")

    exist_user=Data().select_from_table(['user_id'], ['user_id'], [str(user_id)])

    if exist_user==False:
        Data().insert_row(['user_id', 'user_name', 'user_role', 'tokens'], [user_id, user_name,'User', 0])
        logging.info(f"Пользователь с id - {user_id} зарегистрировался в боте как user")
    bot.send_message(message.chat.id, "Приветствую, пользователь!", reply_markup=keyboard1)
    logging.info(f"Отправлено приветственное сообщение пользователю с id - {user_id}")


@bot.message_handler(commands=["logs"])
def log_func(message):
    user_id = message.from_user.id
    logging.info(f"Пользователь с id - {user_id} использовал комманду /log")
    user_role = Data().select_from_table(['user_role'], ['user_id'], [str(user_id)])
    if user_role == "Admin":
        doc = open('log_file.txt', 'rb')
        bot.send_document(message.chat.id, doc)
        logging.warning(f"Пользователю с id - {user_id} отправлен файл с логами")
    else:
        bot.send_message(message.chat.id, text="ливни нахуй с жизни")

    
register_handlers(bot)

@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == config.adm_password:
        user_id = message.from_user.id
        user_name = message.from_user.username
        Data().update_in_table(['user_role'], ['Admin'], ['user_id'], [user_id])
        logging.info(f"Пользователь с id - {user_id} зарегистрировался в боте как admin")
        bot.send_message(message.chat.id, text="Вы зарегистрировались как admin")
    else:
        bot.send_message(message.chat.id, "Используй кнопки для общения с ботом")

bot.polling()