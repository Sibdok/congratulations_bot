import telebot
from info import *
import sqlite3
from datetime import datetime
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton



bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
    encoding='utf-8',
)


MAX_USERS = 50
MAX_TOKENS_FOR_USER = 600
MAX_TOKENS = 60


def create_db():
    logging.info("Создана БД")
    connection = sqlite3.connect('DATABASE.db')
    cur = connection.cursor()
    sql_query = ('CREATE TABLE IF NOT EXISTS users_data (' \
                 'id INTEGER PRIMARY KEY, ' \
                 'user_id INTEGER,' \
                 'user_name TEXT, ' \
                 'user_role TEXT, ' \
                 'tokens INTEGER, ' \
                 'task TEXT)'
                 )
    cur.execute(sql_query)
    connection.close()

def exist_user(user_id):
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    query = f'''SELECT user_id FROM users_data WHERE user_id = {user_id}'''
    results = cur.execute(query)
    try:
        results = results.fetchone()[0]
    except:
        results = None
    connection.close()
    return results == user_id

def is_limit_users():
        global MAX_USERS
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT DISTINCT user_id FROM users_data;')
        count = 0 
        for i in result: 
            count += 1 
        connection.close()
        return count >= MAX_USERS  



keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Написать открытку🖼️').add("Написать поздравление🎉").add("Написать тост🥂")

@bot.message_handler(commands=["start"])
def welcome(message):
    user_id = message.from_user.id
    user_id = message.from_user.id
    user_name = message.from_user.username
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    logging.info(f"Пользователь с id - {user_id} использовал комманду /start")
    if exist_user(user_id):
        logging.info(f"Отправлено приветственное сообщение пользователю с id - {user_id}")
        bot.send_message(message.chat.id, "Приветствую, пользователь!", reply_markup=keyboard1)
        sql_query = "UPDATE users_data SET task = ? WHERE user_id = ?;"
        cur.execute(sql_query, (" ", user_id))
        connection.commit()
    else:
        logging.info(f"Отправлено приветственное сообщение пользователю с id - {user_id}")
        bot.send_message(message.chat.id, "Приветствую, пользователь!", reply_markup=keyboard1)
        sql_query = "UPDATE users_data SET task = ? WHERE user_id = ?;"
        try:
            sql = "INSERT INTO users_data (user_id, user_name, user_role, tokens, task) VALUES (?, ?, ?, ?, ?);"
            data = (user_id, user_name, "User", 0," ")
            cur.execute(sql, data)
            connection.commit()
            logging.info(f"Пользователь с id - {user_id} зарегистрировался в боте как user")
        
        except sqlite3.Error as error:
            logging.warning("Ошибка при работе с SQLite", error)
        
        

    connection.close()


@bot.message_handler(commands=["logs"])
def log_func(message):
    user_id = message.from_user.id
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    logging.info(f"Пользователь с id - {user_id} использовал комманду /log")
    try:
        user_role = cur.execute(f'''SELECT user_role FROM users_data WHERE user_id = {user_id}''').fetchone()[0]
    except:
        logging.warning(f"Пользователю с id - {user_id} не удалость получить его должность")

    if is_limit_users() == False:
        if user_role == "Admin":
            doc = open('log_file.txt', 'rb')
            bot.send_document(message.chat.id, doc)
            logging.warning(f"Пользователю с id - {user_id} отправлен файл с логами")
        else:
            bot.send_message(message.chat.id, text="Вам нельзя использовать эту функцию!")
    else:
        bot.send_message(message.chat.id, text="Извиняемся, но в данный момент бот перегружен!")
        logging.warning("Бот пререгружен")
    connection.close()  
    

@bot.message_handler(content_types=["text"])
def send_text(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    if is_limit_users() == False:
        if message.text == adm_password:
            delite = (f'''DELETE FROM users_data WHERE user_id = {user_id}''')
            cur.execute(delite)
            connection.commit()
            try:
                sql = "INSERT INTO users_data (user_id, user_name, user_role, tokens, task) VALUES (?, ?, ?, ?, ?);"
                data = (user_id, user_name, "Admin", 0, " ")
                cur.execute(sql, data)
                connection.commit()
                bot.send_message(message.chat.id, text="Вы зарегистрировались как admin")
                logging.info(f"Пользователь с id - {user_id} зарегистрировался в боте как admin")
                
            except sqlite3.Error as error:
                logging.warning("Ошибка при работе с SQLite", error)

        elif message.text.lower() == "написать открытку🖼️":
            logging.info(f"Пользователь с id - {user_id} использовал кнопку 'написать открытку🖼️'")
            bot.send_message(message.chat.id, "пососакай")
        elif message.text.lower() == "написать поздравление🎉":
            logging.info(f"Пользователь с id - {user_id} использовал кнопку 'написать поздравление🎉'")
            bot.send_message(message.chat.id, "пососакай дважды")
        elif message.text.lower() == "написать тост🥂":
            logging.info(f"Пользователь с id - {user_id} использовал кнопку 'написать тост🥂'")
            bot.send_message(message.chat.id, "пососакай трижды")
        else:
            logging.info(f"Пользователь с id - {user_id} отправил текстовое сообщение - '{message.text}'")
            bot.send_message(message.chat.id, "Используй кнопки для общения с ботом")


        
        
    connection.close()  

        
create_db()
bot.polling()
