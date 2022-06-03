from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from create_bot import dp, bot
from keyboards import kb_clients_settings, kb_clients
#from Columbia_com import parse
#import time


#@dp.message_handler(commands=["start", "help", "Меню"])
async def commads_start(message: types.CallbackQuery):
    try:
        #await message.answer(message.text)  # тупо отсылает текст
        # await message.reply(message.text) # отвечает, цитируя твое сообщение
        # await bot.send_message(message.from_user.id, message.text) #отправить лично пользователю
        await bot.send_message(message.from_user.id, "Меню", reply_markup=kb_clients)
        #await message.message.delete()
    except:
        pass
        #await message.reply("Общение с ботом через личные сообщения, напишите ему\nhttps://t.me/aleksej_test_my_bot")

async def command_settings(message: types.CallbackQuery):
    await message.message.edit_text('Настройки', reply_markup=kb_clients_settings)
    #await message.message.delete()



def register_handler_clients(dp: Dispatcher):
    dp.register_message_handler(commads_start, commands=["start", "help", "Меню"]) #Можно писать такие функции вместо декораторов
    dp.register_callback_query_handler(commads_start, text=["start", "help", "Меню"])
    #для каждого декоратора дополнительная строка в функции
    dp.register_callback_query_handler(command_settings, text=["Настройки"])


