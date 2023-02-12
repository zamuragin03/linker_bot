from tracemalloc import start
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

help_kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
options = ['Изменить список каналов', 'Поиск по ключевому слову',
           'Список отслеживаемых каналов', 'Список ключевых слов']
for option in options:
    btn = KeyboardButton(text=option)
    help_kb.add(btn)

actions_with_channels_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True)
actions = ['Добавить', 'Удалить']
for option in actions:
    btn = KeyboardButton(text=option)
    actions_with_channels_kb.add(btn)


actions_with_chats_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True)
actions_chats = ['Добавить ключевое слово', 'Удалить ключевое слово',
                 'Добавить канал', 'Список каналов', 'Список ключевых слов']
for option in actions_chats:
    btn = KeyboardButton(text=option)
    actions_with_chats_kb.add(btn)
