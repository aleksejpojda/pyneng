from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot, path
from handlers.admin import chatid
from keyboards.client_keyboard import kb_clients_settings, kb_clients, kb_upload
from Columbia_com import parser_Columbia
from Zara_com import parser_Zara
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
async def command_anonse_file(message: types.CallbackQuery):
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
                    else: my_description=None
            text = f"<b>{line['title']}</b>\n\nЦена: {line['price']} +вес\t\t\t\t\t\t<s>{old_price}</s>\n\n{line['link']}\n\n{my_description}\n"
            await bot.send_photo(chat_id=chatid, photo=line['img'], caption=text, parse_mode="html")
            time.sleep(3)


#@dp.message_handler(commands=list_file_keys)
#async def command_anonse_shop(message: types.Message):
async def command_anonse_shop(message: types.CallbackQuery):
    """Тут показываем список кнопок с файлами для выгрузки"""

    list_file = remove_old_files()
    #kb2_list = list_file[f"/{message.message}"]
    #print(message.data)
    kb2_list = [InlineKeyboardButton(text=line.lstrip('/'), callback_data=line.lstrip('/')) for line in list_file[f"/{message.data}"]]
    #print(kb2_list)
    kb_upload_2 = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*kb2_list).add(InlineKeyboardButton('Меню', callback_data='Меню'))
    await bot.send_message(message.from_user.id, text='Выберите магазин для выгрузки', reply_markup=kb_upload_2)
    #print('keys')
    #file = message.text
    #file = file.lstrip('/')
    #with open(file) as f:
    #    line = yaml.safe_load(f)
    #text = f"<b>{line['title']}</b>\n\n{line['price']}\n\n<a href='{line['img']}' ></a> {line['link']}\n"
    #await bot.send_message(chat_id=chatid, text=text, parse_mode="html")



#@dp.message_handler(commands=["Анонсы"])
#async def command_anonse(message: types.Message):
async def command_anonse(message: types.CallbackQuery):

    remove_old_files()
    #await bot.send_message(message.from_user.id, "/Настройки", reply_markup=ReplyKeyboardRemove(kb_clients))
    ##await message.answer(text="Анонсы", reply_markup=kb_upload)
    #await message.answer('Анонсы', reply_markup=kb_upload)
    await bot.send_message(message.from_user.id, text='Анонсы', reply_markup=kb_upload)
    await message.answer()
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
    #await message.answer(text=f'Сайт Columbia распарсили')
    parser_Zara.parse()
    await message.answer(text='Сайты распарсили')
    remove_old_files()
    #await message.answer(text='Старые файлы удалены')
    list_dir_sites()


def register_handler_anonse(dp: Dispatcher):
    #dp.register_message_handler(command_anonse, commands=["Анонсы"])
    dp.register_callback_query_handler(command_anonse, text=["Анонсы"])
    dp.register_callback_query_handler(command_upload, text=['Выгрузка'])
    dp.register_callback_query_handler(command_anonse_shop, text=list_file_keys)
    dp.register_callback_query_handler(command_anonse_file, text=list_file_value)