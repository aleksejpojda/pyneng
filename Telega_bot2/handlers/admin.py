from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot, chatid
from database import sqlite_db
from keyboards import kb_clients_settings


ID = None

class FSMNewPost(StatesGroup):
    photo = State()
    description = State()
    price = State()
    link = State()
    #chanel_name = State()

#@dp.message_handler(commands=['Имя канала или чата'])
#async def chanel_name(message: types.Message, state: FSMContext):
#    if message.from_user.id == ID:
#        await bot.send_message(chatid, 'Введите название канала или чата, куда будем постить, бот и вы в нем должны быть администраторами')
#        async with state.proxy() as data:
#            data['chanel_name']=message.text
#        await state.finish()

#Получение ID текущего админа группы (писать только в ту группу где вы админ)
#@dp.message_handler(commands=['admin'], is_chat_admin=True)
async def admin_rules(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Что будем настраивать?", reply_markup=kb_clients_settings)
    await message.delete()

#Начало диалога добавления своего поста, просим фото
#@dp.message_handler(commands=["Пост"], state=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMNewPost.photo.set()
        await message.reply("Загрузи фото")

#Ловим фото и пишем в словарь, просим заголовок
#@dp.message_handler(content_types=['photo'], state=FSMNewPost.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMNewPost.next()
        await message.reply("Пишем заголовок сообщения (название товара)")

#Ловит ответ описания, и просим цену
#@dp.message_handler(state=FSMNewPost.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMNewPost.next()
        await message.reply("Укажи цену товара в $")

#Ловим цену и просим ссылку
#@dp.message_handler(state=FSMNewPost.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["price"] = float(message.text)
        await FSMNewPost.next()
        await message.reply("А сюда укажи ссылку на товар")

#Ловим ссылку и финишируем
#@dp.message_handler(state=FSMNewPost.link)
async def load_link(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["link"] = message.text
        async with state.proxy() as data:
            text = f"<b>{data['description']}</b>\n\n{data['price']}\n\n {data['photo']}\n{data['link']}\n"
            #await message.reply(text, parse_mode='html')
            await bot.send_photo(chatid, data['photo'], f"{data['description']}\nЦена: ${data['price']}\n{data['link']}")
            await sqlite_db.sql_add_command(state)
        await state.finish()

#@dp.message_handler(state="*", commands=["отмена"])
#@dp.message_handler(Text(eqaal='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ввод отменен')

def register_handlers_new_message(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=["Пост"], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMNewPost.photo)
    dp.register_message_handler(load_description, state=FSMNewPost.description)
    dp.register_message_handler(load_price, state=FSMNewPost.price)
    dp.register_message_handler(load_link, state=FSMNewPost.link)
    dp.register_message_handler(cancel_handler, state="*", commands=["отмена"])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin_rules, commands=['admin'], is_chat_admin=True)
#    dp.register_message_handler(chanel_name, commands=['Имя канала или чата'])