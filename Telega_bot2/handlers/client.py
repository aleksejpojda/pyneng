from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from create_bot import dp, bot
from keyboards import kb_clients_settings, kb_clients
#from Columbia_com import parse
#import time


#@dp.message_handler(commands=["start", "help", "Меню"])
async def commads_start(message: types.Message):
    try:
        #await message.answer(message.text)  # тупо отсылает текст
        # await message.reply(message.text) # отвечает, цитируя твое сообщение
        # await bot.send_message(message.from_user.id, message.text) #отправить лично пользователю
        await message.answer(text="Привет", allow_sending_without_reply=True, reply_markup=kb_clients)
        await message.delete()
    except:
        pass
        #await message.reply("Общение с ботом через личные сообщения, напишите ему\nhttps://t.me/aleksej_test_my_bot")

async def command_settings(message: types.Message):
    await message.answer(allow_sending_without_reply=True, text='Настройки', reply_markup=kb_clients_settings)
    #await message.delete()



def register_handler_clients(dp: Dispatcher):
    dp.register_message_handler(commads_start, commands=["start", "help", "Меню"]) #Можно писать такие функции вместо декораторов
    #для каждого декоратора дополнительная строка в функции
    dp.register_message_handler(command_settings, commands=["Настройки"])


