import telebot
from info import *
# from iam import *
import requests
import sqlite3
from datetime import datetime
import logging
from fusion import *
from DataBase import Data


bot = telebot.TeleBot(TOKEN)


# iam_token = iam_token

MAX_USERS = 50
MAX_TOKENS = 120

def count_tokens(message):
    user_id = message.from_user.id
    user_data=Data().select_from_table(['*'], ['user_id'], [str(user_id)], return_all=True)
    task = user_data[0][6]
    
    print(task)

    headers = { # заголовок запроса, в котором передаем IAM-токен
        'Authorization': f'Bearer {iam_token}', # token - наш IAM-токен
        'Content-Type': 'application/json'
    }
    data = {
       "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest", # указываем folder_id
       "maxTokens": MAX_TOKENS,
       "text": task
    }
    tokens=Data().select_from_table(['tokens'],['user_id'], [str(user_id)])
    print(tokens)
    int(str(tokens))
    print(len(requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",json=data, headers=headers).json()['tokens']))
    new_tokens = tokens + len(requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",json=data, headers=headers).json()['tokens'])
    Data().update_in_table(['tokens'], [new_tokens], ['user_id'], [user_id])
    ask_gpt(message)


def ask_gpt(message):
    user_id = message.from_user.id

    user_data=Data().select_from_table(['*'], ['user_id'], [str(user_id)], return_all=True)
    task = user_data[0][6]

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
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        tokens=Data().select_from_table(['tokens'], ['user_id'], [str(user_id)])
        new_tokens = tokens + MAX_TOKENS
        Data().update_in_table(['tokens'], [new_tokens], ['user_id'], [user_id])
        rec=Data().select_from_table(['request'], ['user_id'], [str(user_id)])

        if rec == 1:
            bot.send_message(message.chat.id, text=f"{text}")
            logging.info(f"Пользователю с id - {user_id} было отправлено поздравление")
        elif rec == 2:
            bot.send_photo(message.chat.id, promt(task), text)
            logging.info(f"Пользователю с id - {user_id} была отправлена открытка")
        return text
    
    else:
        logging.warning(RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {response.status_code}, {response.text}
            )
        ))
