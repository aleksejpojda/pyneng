import yaml
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from files import list_dir_sites

#list_dir_sites()

b1 = KeyboardButton('/Настройки')
b2 = KeyboardButton('/Анонсы')
b3 = KeyboardButton('/Приветствия')
b4 = KeyboardButton('/Шаблоны')

kb_clients = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b1, b2).row(b3, b4)
#Размещаем кнопки в 2 строки и 2 столбца

b_s1 = KeyboardButton('/Валюта')
b_s2 = KeyboardButton("/Формула ценообразования")
b_s3 = KeyboardButton("/Пост")
b_s4 = KeyboardButton("/Имя канала или чата")
b_s5 = KeyboardButton("/Моя подпись")
b_s6 = KeyboardButton("/Язык")
b_s7 = KeyboardButton("/Короткая ссылка")
b_s8 = KeyboardButton("/Выгрузка")

kb_clients_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_clients_settings.add(b_s1).insert(b_s2).add(b_s3).insert(b_s4).add(b_s5).insert(b_s6).add(b_s7).insert(b_s8).add(KeyboardButton('/Меню'))

with open('file_list.yaml') as f:
    list_file = yaml.safe_load(f)
    list_kb_vlaue = []
for line in list_file.values():
    list_kb_vlaue.extend(line)

kb_upload = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).row(*list_file.keys()).add(KeyboardButton('/Меню'))
#kb_upload_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).row(*list_kb_vlaue)