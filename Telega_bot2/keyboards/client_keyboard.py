import yaml
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


b1 = InlineKeyboardButton(text='Настройки', callback_data='Настройки')
b2 = InlineKeyboardButton(text='Анонсы', callback_data='Анонсы')
b3 = InlineKeyboardButton(text='Приветствия', callback_data='Приветствия')
b4 = InlineKeyboardButton(text='Шаблоны', callback_data='Шаблоны')

kb_clients = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b1, b2).row(b3, b4)
#Размещаем кнопки в 2 строки и 2 столбца

b_s1 = InlineKeyboardButton('Валюта', callback_data='Валюта')
b_s2 = InlineKeyboardButton("Формула ценообразования", callback_data='Формула_ценообразования')
b_s3 = InlineKeyboardButton("Пост", callback_data='Пост')
b_s4 = InlineKeyboardButton("Имя канала или чата", callback_data='Имя_канала_или_чата')
b_s5 = InlineKeyboardButton("Моя подпись", callback_data='Моя_подпись')
b_s6 = InlineKeyboardButton("Язык", callback_data='Язык')
b_s7 = InlineKeyboardButton("Короткая ссылка", callback_data='Короткая_ссылка')
b_s8 = InlineKeyboardButton("Выгрузка", callback_data='Выгрузка')

kb_clients_settings = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_clients_settings.add(b_s1).insert(b_s2).add(b_s3).insert(b_s4).add(b_s5).insert(b_s6)\
    .add(b_s7).insert(b_s8).add(InlineKeyboardButton('Меню', one_time_keyboard=True, callback_data='Меню'))

with open('file_list.yaml') as f:
    list_file = yaml.safe_load(f)
    list_kb_vlaue = []
for line in list_file.values():
    list_kb_vlaue.extend(line)

button_list = [InlineKeyboardButton(text=line.lstrip('/'), callback_data=line.lstrip('/')) for line in list_file.keys()]



kb_upload = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)\
    .row(*button_list).add(InlineKeyboardButton('Меню', callback_data='Меню'))

short_long_button = [InlineKeyboardButton(text='Обычная ссылка', callback_data='long'), InlineKeyboardButton(text='Короткая ссылка', callback_data='short')]
kb_short_long_link = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)\
    .row(*short_long_button).add(InlineKeyboardButton(text='Меню', callback_data='Меню'))