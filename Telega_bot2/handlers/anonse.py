from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from create_bot import dp, bot, path
from handlers.admin import chatid
from keyboards.client_keyboard import kb_clients_settings, kb_clients, kb_upload
from Columbia_com import parser_Columbia
import time, yaml, csv, os
from files import remove_old_files, list_dir_sites


list_file_value = []
with open('file_list.yaml') as f:
    list_file = yaml.safe_load(f)
    list_file_keys = [key.lstrip('/') for key in list_file.keys()]
#print(list_file_keys, '*********')
    for line in list_file.values():
        list_file_value.extend(line)
        list_file_value = [file.lstrip('/') for file in list_file_value]
#list_file_value.extend = [lists for lists in list_file.values()]
#print(list_file_value, '888888')

#@dp.message_handler(commands=list_file_value)
async def command_anonse_file(message: types.Message):
    #print('value')
    with open(message.text.lstrip('/')) as f:
        reader = csv.DictReader(f, delimiter=";")
        for line in reader:
            if line['old_price']:
                old_price = line['old_price']
            else: old_price = None
            files = [f for f in os.listdir(path) if os.path.isfile(f)]
            if 'settings.yaml' in files:
                with open('settings.yaml', 'r') as f:
                    settings = yaml.safe_load(f)
                    for row in settings:
                        if row['my_description']:
                            my_description = row['my_description']
                        else: my_description=None
            text = f"<b>{line['title']}</b>\n\n{line['price']}\t\t\t\t\t\t<s>{old_price}</s>\n\n<a href='{line['img']}' ></a> {line['link']}\n\n{my_description}\n"
            await bot.send_message(chat_id=chatid, text=text, parse_mode="html")
            time.sleep(3)


#@dp.message_handler(commands=list_file_keys)
async def command_anonse_shop(message: types.Message):
    """Тут показываем список кнопок с файлами для выгрузки"""

    list_file = remove_old_files()
    kb2_list = list_file[message.text]
    kb_upload_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*kb2_list).add(KeyboardButton('/Меню'))
    await message.answer(text='Выберите магазин для выгрузки', reply_markup=kb_upload_2)
    #print('keys')
    #file = message.text
    #file = file.lstrip('/')
    #with open(file) as f:
    #    line = yaml.safe_load(f)
    #text = f"<b>{line['title']}</b>\n\n{line['price']}\n\n<a href='{line['img']}' ></a> {line['link']}\n"
    #await bot.send_message(chat_id=chatid, text=text, parse_mode="html")



#@dp.message_handler(commands=["Анонсы"])
async def command_anonse(message: types.Message):
    remove_old_files()
    #await bot.send_message(message.from_user.id, "/Настройки", reply_markup=ReplyKeyboardRemove(kb_clients))
    await message.answer(text="Анонсы", reply_markup=kb_upload)
    #out = parse()
    #print(out)

    #for line in out:
    #    if line["old_price"]:
    #        text = f"<b>{line['title']}</b>\n\n{line['price']}\t\t\t\t\t\t<s>{line['old_price']}</s>\n\n<a href='{line['img']}' ></a> {line['link']}\n"
    #    else:
    #        text = f"<b>{line['title']}</b>\n\n{line['price']}\n\n<a href='{line['img']}' ></a> {line['link']}\n"
    #    #await message.answer(allow_sending_without_reply=True, text=text, parse_mode="html")
    #    await bot.send_message(chat_id=chatid, text=text, parse_mode="html")
    #    time.sleep(3)
    #await message.delete()

async def command_upload(message: types.Message):
    parser_Columbia.parse()
    await message.answer(text='Сайт Columbia распарсили')
    remove_old_files()
    await message.answer(text='Старые файлы удалены')
    list_dir_sites()


def register_handler_anonse(dp: Dispatcher):
    dp.register_message_handler(command_anonse, commands=["Анонсы"])
    dp.register_message_handler(command_upload, commands=['Выгрузка'])
    dp.register_message_handler(command_anonse_shop, commands=list_file_keys)
    dp.register_message_handler(command_anonse_file, commands=list_file_value)