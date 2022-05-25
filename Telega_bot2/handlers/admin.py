import yaml, os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot#, chatid
from database import sqlite_db
from create_bot import path
from keyboards import kb_clients_settings


# Читаем настройки из файла если он есть,
# если нет, то имя канала по умолчанию @my_test_chanal_1
files = [f for f in os.listdir(path) if os.path.isfile(f)]
if 'settings.yaml' in files:
    with open('settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)
        print('Считываем настройки...')
        if 'chatid' in settings:
            chatid=settings['chatid']
            print(f'нашли chatid {chatid}')
        else: chatid = "@my_test_chanal_1"
else: chatid = "@my_test_chanal_1"

#ID = None

class FSMNewPost(StatesGroup):
    photo = State()
    description = State()
    price = State()
    link = State()

class FSMSettings(StatesGroup):
    my_description = State()

class FSMSettingsChatID(StatesGroup):
    chatid = State()

#@dp.message_handler(commands=['Имя канала или чата'])
#async def chanel_name(message: types.Message, state: FSMContext):
#    if message.from_user.id == ID:
#        await bot.send_message(chatid, 'Введите название канала или чата, куда будем постить, бот и вы в нем должны быть администраторами')
#        async with state.proxy() as data:
#            data['chanel_name']=message.text
#        await state.finish()

#Получение ID текущего админа группы (писать только в ту группу где вы админ)
#@dp.message_handler(commands=['admin'], is_chat_admin=True)
#async def admin_rules(message: types.Message):
#    global ID
#    ID = message.from_user.id
#    await bot.send_message(message.from_user.id, "Что будем настраивать?", reply_markup=kb_clients_settings)
#    await message.delete()

#Начало диалога добавления своего поста, просим фото
#@dp.message_handler(commands=["Пост"], state=None)
async def cm_start(message : types.Message):
    #if message.from_user.id == ID:
    await FSMNewPost.photo.set()
    await message.reply("Загрузи фото")

#Ловим фото и пишем в словарь, просим заголовок
#@dp.message_handler(content_types=['photo'], state=FSMNewPost.photo)
async def load_photo(message: types.Message, state: FSMContext):
    #if message.from_user.id == ID:
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMNewPost.next()
    await message.reply("Пишем заголовок сообщения (название товара)")

#Ловит ответ описания, и просим цену
#@dp.message_handler(state=FSMNewPost.description)
async def load_description(message: types.Message, state: FSMContext):
    #if message.from_user.id == ID:
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMNewPost.next()
    await message.reply("Укажи цену товара в $")

#Ловим цену и просим ссылку
#@dp.message_handler(state=FSMNewPost.price)
async def load_price(message: types.Message, state: FSMContext):
    #if message.from_user.id == ID:
    async with state.proxy() as data:
        data["price"] = float(message.text)
    await FSMNewPost.next()
    await message.reply("А сюда укажи ссылку на товар")

#Ловим ссылку и финишируем
#@dp.message_handler(state=FSMNewPost.link)
async def load_link(message: types.Message, state: FSMContext):
    #if message.from_user.id == ID:
    async with state.proxy() as data:
        data["link"] = message.text
    async with state.proxy() as data:
        files = [f for f in os.listdir(path) if os.path.isfile(f)]
        if 'settings.yaml' in files:
            with open('settings.yaml', 'r') as f:
                settings = yaml.safe_load(f)
                for line in settings:
                    if line['my_description']:
                        my_description = line['my_description']
                    else:
                        my_description = None
        #await message.reply(text, parse_mode='html')
        await bot.send_photo(chatid, data['photo'], f"{data['description']}\nЦена: ${data['price']}\n{data['link']}\n\n{my_description}\n")
        await sqlite_db.sql_add_command(state)
    await state.finish()

#@dp.message_handler(state="*", commands=["отмена"])
#@dp.message_handler(Text(eqaal='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """Делаем отмену"""
    #if message.from_user.id == ID:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ввод отменен')

#@dp.message_handler(commands=['Моя_подпись'])
async def my_description(message: types.Message):
    """Просим настройки подписи"""
    await FSMSettings.my_description.set()
    await message.reply('Введите подпись, будет отображаться в каждом сообщении')



async def save_msg_setting(message: types.Message, state: FSMContext):
    """Получаем сообщение с текстом настроек подписи"""
    async with state.proxy() as data:
        await write_setting(message.text, "my_description")
    await state.finish()

#@dp.message_handler(commands=['Имя_канала_или_чата'])
async def my_chatid(message: types.Message):
    """Просим настройки имени канала"""
    await FSMSettingsChatID.chatid.set()
    await message.reply('Введите имя канала, в котором бот будет постить сообщения')

async def save_chatid_setting(message: types.Message, state: FSMContext):
    """Получаем мия канала"""
    async with state.proxy() as data:
        await write_setting(message.text, "chatid")
    await state.finish()

async def write_setting(message, name_setting):
    """Записываем настройки в файл"""
    files = [f for f in os.listdir(path) if os.path.isfile(f)]
    if 'settings.yaml' in files:
        with open('settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)
            if not settings:
                settings = {}
            settings[name_setting] = message
    with open('settings.yaml', 'w') as f:
        yaml.dump(settings, f, default_flow_style=False)



def register_handlers_new_message(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=["Пост"], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMNewPost.photo)
    dp.register_message_handler(cancel_handler, state="*", commands=["отмена"])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_description, state=FSMNewPost.description)
    dp.register_message_handler(load_price, state=FSMNewPost.price)
    dp.register_message_handler(load_link, state=FSMNewPost.link)
    dp.register_message_handler(my_description, commands=['Моя_подпись'])
    dp.register_message_handler(save_msg_setting, state=FSMSettings.my_description)
    dp.register_message_handler(my_chatid, commands=['Имя_канала_или_чата'])
    dp.register_message_handler(save_chatid_setting, state=FSMSettingsChatID.chatid)
#    dp.register_message_handler(admin_rules, commands=['admin'], is_chat_admin=True)
#    dp.register_message_handler(chanel_name, commands=['Имя канала или чата'])