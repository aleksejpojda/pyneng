from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot, path
from handlers.admin import chatid
from keyboards.client_keyboard import kb_clients_settings, kb_clients, kb_upload
from Columbia_com import parser_Columbia
from Zara_com import parser_Zara
from SixPM_com import parser_6pm
from Amazon_com import parser_Amazon
import time, yaml, csv, os
from files import remove_old_files, list_dir_sites
from short_link import short_url


def list_files(key=None, value=None):
    list_file_value = []
    with open('file_list.yaml') as f:
        list_file = yaml.safe_load(f)
        list_file_keys = [key.lstrip('/') for key in list_file.keys()]
    #print(list_file_keys, '*********')
        for line in list_file.values():
            list_file_value.extend(line)
            list_file_value = [file.lstrip('/') for file in list_file_value]
    if key == "key":
        return list_file_keys
    elif value == 'value':
        return list_file_value
#list_file_value.extend = [lists for lists in list_file.values()]
#print(list_file_value, '888888')

#@dp.message_handler(commands=list_file_value)
async def command_anonse_file(message: types.CallbackQuery):
    """отправка анонсов в чат"""
    #print('value')
    with open(message.data.lstrip('/')) as f:
        reader = csv.DictReader(f, delimiter=";")
        for line in reader:
            if "old_price" in line.keys() and line['old_price']:
                old_price = line['old_price']
            else: old_price = ''
            files = [f for f in os.listdir(path) if os.path.isfile(f)]
            if 'settings.yaml' in files:
                with open('settings.yaml', 'r') as f:
                    settings = yaml.safe_load(f)
                    if settings['my_description']:
                        my_description = settings['my_description']
                    else: my_description = None
                    if settings['chatid']:
                        chatid = settings['chatid']
                    if settings['short_url'] and settings['short_url'] == 'short':
                        link = short_url(line['link'])
                    elif not settings['short_url'] or settings['short_url'] == 'long':
                        link = line['link']
            text = f"<b>{line['title']}</b>\n\nЦена: {line['price']} +вес\t\t\t\t\t\t" \
                   f"<s>{old_price}</s>\n\n{link}\n\n{my_description}\n"
            await bot.send_photo(chat_id=chatid, photo=line['img'], caption=text, parse_mode="html")
            time.sleep(13)
        await message.message.answer('Все сообщения оправлены')


#@dp.message_handler(commands=list_file_keys)
#async def command_anonse_shop(message: types.Message):
async def command_anonse_shop(message: types.CallbackQuery):
    """Тут показываем список кнопок с файлами для выгрузки"""

    list_file = remove_old_files()
    kb2_list = [
        InlineKeyboardButton(text=line.lstrip('/'), callback_data=line.lstrip('/'))
        for line in list_file[f"/{message.data}"]
        ]
    kb_upload_2 = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)\
        .add(*kb2_list).add(InlineKeyboardButton('Меню', callback_data='Меню'))
    await message.message.edit_text("Выберите файл для отправки анонсов", reply_markup=kb_upload_2)


#@dp.message_handler(commands=["Анонсы"])
#async def command_anonse(message: types.Message):
async def command_anonse(message: types.CallbackQuery):
    """показать кнопки со списком магазмнов"""
    await message.message.edit_text("Выберите магазин для отправки анонсов", reply_markup=kb_upload)
    await message.answer()


async def command_upload(message: types.CallbackQuery):
    """Выгрузка"""
    await message.message.answer(text='Работаем')
    parser_Columbia.parse()
    await message.message.answer(text='Сайт Columbia.com распарсили')
    parser_Zara.parse()
    await message.message.answer(text='Сайт Zara.com распарсили')
    parser_6pm.parse()
    await message.message.answer(text='Сайт 6pm.com распарсили')
    parser_Amazon.parse()
    await message.message.answer(text='Сайт Amazon.com распарсили')
    remove_old_files(remove=True)
    await message.message.answer(text='Старые файлы удалены')
    list_dir_sites()
    register_handler_anonse(dp)


def register_handler_anonse(dp: Dispatcher):
    list_file_keys = list_files(key ='key')
    list_file_value = list_files(value='value')
    #dp.register_message_handler(command_anonse, commands=["Анонсы"])
    dp.register_callback_query_handler(command_anonse, text=["Анонсы"])
    dp.register_callback_query_handler(command_upload, text=['Выгрузка'])
    dp.register_callback_query_handler(command_anonse_shop, text=list_file_keys)
    dp.register_callback_query_handler(command_anonse_file, text=list_file_value)