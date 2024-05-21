import telebot
from info import *
# from iam import *
import requests
import sqlite3
from datetime import datetime
import logging
from fusion import *

bot = telebot.TeleBot(TOKEN)


# iam_token = iam_token

MAX_USERS = 50
MAX_TOKENS = 120

def count_tokens(message):
    user_id = message.from_user.id
    connection = sqlite3.connect('DATABASE.db')
    cur = connection.cursor()
    user_data = cur.execute(f'''SELECT * FROM users_data WHERE user_id = {user_id}''').fetchone()
    task = user_data[6]
    
    print(task)


    token = iam_token
    headers = { # заголовок запроса, в котором передаем IAM-токен
        'Authorization': f'Bearer {token}', # token - наш IAM-токен
        'Content-Type': 'application/json'
    }
    data = {
       "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest", # указываем folder_id
       "maxTokens": MAX_TOKENS,
       "text": task
    }
    tokens = cur.execute(f'''SELECT tokens FROM users_data WHERE user_id = {user_id}''').fetchone()[0]
    int(str(tokens))
    


    new_tokens = tokens + len(requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",json=data, headers=headers).json()['tokens'])

    sql_query = "UPDATE users_data SET tokens = ? WHERE user_id = ?;"
    cur.execute(sql_query, (new_tokens, user_id))
    connection.commit()
    tokens = cur.execute(f'''SELECT tokens FROM users_data WHERE user_id = {user_id}''').fetchone()[0]
    ask_gpt(message)


def ask_gpt(message):
    user_id = message.from_user.id
    connection = sqlite3.connect('DATABASE.db')
    cur = connection.cursor()

    user_data = cur.execute(f'''SELECT * FROM users_data WHERE user_id = {user_id}''').fetchone()
    task = user_data[6]

    print(task)
    
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",  
        "completionOptions": {
            "stream": False,  
            "temperature": 0.6,  
            "maxTokens": MAX_TOKENS
        },
        "messages": [
            {
                "role": "user",  
                "text": task
            }
        ]
    }

    # Выполняем запрос к YandexGPT
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                             headers=headers,
                             json=data)
    
    # Проверяем, не произошла ли ошибка при запросе
    if response.status_code == 200:
        user_id = message.from_user.id
        connection = sqlite3.connect('DATABASE.db')
        cur = connection.cursor()
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        
        tokens = cur.execute(f'''SELECT tokens FROM users_data WHERE user_id = {user_id}''').fetchone()[0]
        new_tokens = tokens + MAX_TOKENS
        sql_query = "UPDATE users_data SET tokens = ? WHERE user_id = ?;"
        cur.execute(sql_query, (new_tokens, user_id))

        rec = cur.execute(f'''SELECT request FROM users_data WHERE user_id = {user_id}''').fetchone()[0]

        connection.commit()
        connection.close()

        if rec == 1:
            bot.send_message(message.chat.id, text=f"{text}")
            logging.info(f"Пользователю с id - {user_id} было отправлено поздравление")
        elif rec == 2 :
            bot.send_photo(message.chat.id, promt(task), text)
            logging.info(f"Пользователю с id - {user_id} была отправлена открытка")
        



        
        return text
    
    else:
        logging.warning(RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {response.status_code}, {response.text}
            )
        ))
