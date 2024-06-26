import telebot
from info import *
from gpt import *
import sqlite3
from datetime import datetime
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fusion import *


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
        Data().update_in_table(['task'], [f'Напиши поздравление для {message.text}'], ['user_id'], [user_id])
        bot.send_message(message.chat.id, "Напиши с чем ты хочешь его поздравить:")
        bot.register_next_step_handler(message, occasion)

    def occasion(message):
        print("occasion")
        user_id = message.from_user.id
        user_name = message.from_user.username
        task=Data().select_from_table(['task'], ['user_id'], [str(user_id)])
        Data().update_in_table(['task'],[f"{task}. Поздравь его с {message.text}"], ['user_id'], [user_id])
        Data().update_in_table(['request'], [1], ['user_id'], [user_id])
        logging.info(f"Пользователь с id - {user_id} отправил запрос к YaGPT для создания поздравления")
        count_tokens(message)



    @bot.message_handler(func=lambda message: message.text.lower() == "написать открытку🖼️") 
    def first_ph(message):
        print("first")
        user_id = message.from_user.id
        user_name = message.from_user.username
        logging.info(f"Пользователь с id - {user_id} использовал кнопку 'написать открытку🖼️'")
        bot.send_message(message.chat.id, "Напиши для кого будет поздравление:")
        bot.register_next_step_handler(message, name_ph)
        
    def name_ph(message):
        print("name")
        user_id = message.from_user.id
        user_name = message.from_user.username
        Data().update_in_table(['task'], [f"Напиши поздравление для {message.text}"], ['user_id'], [user_id])
        bot.send_message(message.chat.id, "Напиши с чем ты хочешь его поздравить:")
        bot.register_next_step_handler(message, occasion_ph)

    def occasion_ph(message):
        print("occasion")
        user_id = message.from_user.id
        user_name = message.from_user.username
        task=Data().select_from_table(['task'], ['user_id'], [str(user_id)])
        Data().update_in_table(['task'], [f"{task}. Поздравь его с {message.text}"], ['user_id'], [user_id])
        Data().update_in_table(['request'], [2], ['user_id'], [user_id])
        logging.info(f"Пользователь с id - {user_id} отправил запрос к YaGPT для создания открытки")
        count_tokens(message)



    
    @bot.message_handler(func=lambda message: message.text.lower() == "написать тост🥂") 
    def first_toast(message):
        print("first")
        user_id = message.from_user.id
        user_name = message.from_user.username
        logging.info(f"Пользователь с id - {user_id} использовал кнопку 'написать тост🥂'")
        bot.send_message(message.chat.id, "Напиши по какому поводу нужен тост:")
        bot.register_next_step_handler(message, name_toast)
        
    def name_toast(message):
        print("name")
        user_id = message.from_user.id
        user_name = message.from_user.username
        Data().update_in_table(['task'], [f"Напиши тост по поводу {message.text}"], ['user_id'], [user_id])
        bot.send_message(message.chat.id, "Напиши для кого будет поздравление:")
        bot.register_next_step_handler(message, occasion_toast)

    def occasion_toast(message):
        print("occasion")
        user_id = message.from_user.id
        user_name = message.from_user.username
        task=Data().select_from_table(['task'], ['user_id'], [user_id])
        Data().update_in_table(['task'], [f"{task}. Поздравь {message.text} с этим праздником."], ['user_id'], [user_id])
        Data().update_in_table(['request'], [1], ['user_id'], [user_id])
        logging.info(f"Пользователь с id - {user_id} отправил запрос к YaGPT для создания поздравления")
        count_tokens(message)

    @bot.message_handler(func=lambda message: message.text.lower() == "написать конкурс🎈") 
    def first_con(message):
        print("first")
        user_id = message.from_user.id
        user_name = message.from_user.username
        logging.info(f"Пользователь с id - {user_id} использовал кнопку 'конкурс🎈'")
        bot.send_message(message.chat.id, "Напиши по какому поводу нужен конкурс:")
        bot.register_next_step_handler(message, name_con)
        
    def name_con(message):
        print("name")
        user_id = message.from_user.id
        user_name = message.from_user.username
        Data().update_in_table(['task'], [f"Напиши одно задание на конкурс на {message.text}"], ['user_id'], [user_id])
        occasion_con(message)

    def occasion_con(message):
        print("occasion")
        user_id = message.from_user.id
        user_name = message.from_user.username
        task=Data().select_from_table(['task'], ['user_id'], [user_id])
        Data().update_in_table(['task'], [f"{task} для гостей."], ['user_id'], [user_id])
        Data().update_in_table(['request'], [1], ['user_id'], [user_id])
        logging.info(f"Пользователь с id - {user_id} отправил запрос к YaGPT для создания поздравления")
        count_tokens(message)